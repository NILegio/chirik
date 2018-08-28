from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods
from django.template.context_processors import csrf
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse
import json

from .models import Character, Blog, Commentary, HashtagList
from aas.form import BlogForm, CommentForm, MyUserCreationForm
from aas.parser import hasa, hash_list

from aas.models import HashtagList
from django.core.exceptions import ObjectDoesNotExist
from pyparsing import Word, alphanums, Combine


#class IndexView(LoginRequiredMixin, ListView):
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    blog_form = BlogForm
    login_url = 'login'
    #redirect_field_name = 'login' # в урл добавление

    # paginate_by = 10      # пагинация для листвью
    #
    # def get_queryset(self):
    #
    #     user = auth.get_user(self.request)
    #     chiriks = Blog.objects.filter(owner__username=user.username)
    #     chiriks_friends = Blog.objects.filter(owner__in=user.friends.all())
    #     all_blogs = (chiriks | chiriks_friends).order_by('pub_date').reverse()
    #     return all_blogs

    # def get(self, request, *args, **kwargs):            # попытка в редирект c помощью редирект get
    #     if not self.request.user.is_authenticated:
    #         return redirect('login')

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update(csrf(self.request))
            user = auth.get_user(self.request)
            chiriks = Blog.objects.filter(owner__username=user.username)
            chiriks_friends = Blog.objects.filter(owner__in=user.friends.all())
            #context['blogs'] = (chiriks | chiriks_friends).order_by('pub_date').reverse()
            #context['blogs'] = (chiriks | chiriks_friends).order_by('pub_date').reverse()[:10]
            all_blogs = (chiriks | chiriks_friends).order_by('pub_date').reverse()
            context['blogs'] = all_blogs
            current_page = Paginator(all_blogs, 10)
            page = self.request.GET.get('page')
            try:
                context['blogs'] = current_page.page(page)
            except PageNotAnInteger:
                context['blogs'] = current_page.page(1)
            except EmptyPage:
                context['blogs'] = current_page.page(current_page.num_pages)
            context['form'] = self.blog_form
            context['people'] = Character.objects.exclude(friends_by=user.id).exclude(username=user.username)
        return context


class UserView(DetailView):
#class UserView(IndexView):
    template_name = 'user.html'
    model = Character
    blog_form = BlogForm

    def get_object(self):
        try:
            idi = self.model.objects.get(username=self.kwargs['username'])
        except Character.DoesNotExist:
            raise Http404
        return self.model.objects.get(pk=idi.pk)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        #context['blogs'] = (char.blog.all()).order_by('pub_date').reverse()[:10]
        all_blogs = (char.blog.all()).order_by('pub_date').reverse()
        current_page = Paginator(all_blogs, 10)
        page = self.request.GET.get('page')
        try:
            context['blogs'] = current_page.page(page)
        except PageNotAnInteger:
            context['blogs'] = current_page.page(1)
        except EmptyPage:
            context['blogs'] = current_page.page(current_page.num_pages)
        context['people'] = Character.objects.exclude(friends_by=user.id).exclude(username=user.username)
        # if user.username != char.username:
        #     context['check'] = not char.friends_by.filter(username=user.username)#если друг ээтому человеку даст непустое
        #                                                                 #  значение и код не вывыдет кнопку

        if user.username == char.username:
        #     context['follow'] = 'blank'  # позорище

        #if user.is_authenticated and user.username == char.username:
            context['form'] = self.blog_form

        return context


class UserEditView(UpdateView):
    template_name = 'edit_user.html'
    model = Character
    fields = ('first_name', 'last_name',)

    def get_object(self):
        try:
            idi = self.model.objects.get(username=self.kwargs['username'])
        except Character.DoesNotExist:
            raise Http404
        return self.model.objects.get(pk=idi.pk)

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        user = auth.get_user(self.request)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['people'] = Character.objects.exclude(friends_by=user.id).exclude(username=user.username)
        # context['follow'] = char.friends_by.filter(username=user.username)
        # if user.username == char.username:
        #     context['follow'] = 'blank'  # позорище
        return context

    def get_success_url(self):
        return reverse_lazy('aas:user', args=[str(self.kwargs['username'])])


class ArticlesView(TemplateView):

    template_name = 'comments.html'
    comment_form = CommentForm

    def get_context_data(self, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        blog = get_object_or_404(Blog, id=kwargs['id'])
        user = auth.get_user(self.request)
        context.update(csrf(self.request))
        context['blog'] = blog
        context['comments'] = blog.commentary.all().order_by('id')
        context['next'] = blog.get_absolute_url()
        if user.is_authenticated:
            context['form'] = self.comment_form
        return context


class HashView(TemplateView):
    template_name = 'hashtag.html'

    def get_context_data(self, **kwargs):
        context = super(HashView, self).get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(hashtag_b__hashtag=self.kwargs['hashtag'])
        context['bebe'] = self.kwargs['hashtag']
        return context


class FriendsView(ListView):
    template_name = 'friends.html'
    model = Character

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['people'] = Character.objects.exclude(friends_by=char.id).exclude(username=char.username)
        return context


class RegView(FormView):
    template_name = 'reg/registration.html'
    form_class = MyUserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super(RegView, self).form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'reg/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):

    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect('/')


@login_required
@require_http_methods(["POST"])
def add_writing(request, username):
    form = BlogForm(request.POST)
    character = get_object_or_404(Character, username=username)
    if form.is_valid():
        writing = Blog()
        writing.owner = auth.get_user(request)
        text = hasa.transformString(form.cleaned_data['blog_area'])
        writing.text = text     # не забыть насторить защиту от XSS
        writing.save()
        writing.hashtag_b.add(*hash_list)
    return redirect(character.get_absolute_url())


@login_required
@require_http_methods(["POST"])
def add_comment(request, username, id):
    form = CommentForm(request.POST)
    blog = get_object_or_404(Blog, id=id)

    if form.is_valid():
        comment = Commentary()
        comment.path = []
        comment.blog = blog
        comment.owner = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()

        # try:
        #     comment.path.extend(Commentary.objects.get(id=form.cleaned_data['parent_comment']).path)
        #     comment.path.append(comment.id)
        # except ObjectDoesNotExist:
        #     comment.path.append(comment.id)
        #
        # comment.save()

    return redirect(blog.get_absolute_url())


# @login_required(login_url='login')
# @require_http_methods(["POST"])
# def follow(request, username):
#     user = auth.get_user(request)
#     follower = Character.objects.get(username=username)
#     user.friends.add(follower)
#     return redirect('/')

class FollowView(View):

    model = Character

    def get_object(self):
        try:
            idi = self.model.objects.get(username=self.kwargs['username'])
        except Character.DoesNotExist:
            raise Http404
        return self.model.objects.get(pk=idi.pk)


    def post(self, request, username):
        user = auth.get_user(request)
        follower = Character.objects.get(username=username)
        if user.friends.filter(username=follower.username):
            user.friends.remove(follower)
        else:
            user.friends.add(follower)

        return HttpResponse(
            json.dumps({
                'following' : user.friends.all().count(),
                'followers' : user.friends_by.all().count()
            }),
            content_type='application/json'
        )


def curry(_curried_func, *args, **kwargs):
    # для подключения моих страниц с ошибками
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*(args + moreargs), **dict(kwargs, **morekwargs))
    return _curried
