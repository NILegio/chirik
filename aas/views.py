from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods
from django.template.context_processors import csrf
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy
from django.template import RequestContext
from django.http import HttpResponseNotFound

from .models import Character, Blog, Commentary, HashtagList
from aas.form import BlogForm, CommentForm, MyUserCreationForm



class IndexView(TemplateView):
    template_name = 'index.html'
    blog_form = BlogForm

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update(csrf(self.request))
            user = auth.get_user(self.request)
            chiriks = Blog.objects.filter(owner__username=user.username)
            chiriks_friends = Blog.objects.filter(owner__in=user.friends.all())
            context['blogs'] = (chiriks | chiriks_friends).order_by('pub_date').reverse()[:10]
            context['form'] = self.blog_form
            context['people'] = Character.objects.exclude(friends_by=user.id).exclude(username=user.username)
        return context


class UserView(DetailView):
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
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['blogs'] = (char.blog.all()).order_by('pub_date').reverse()[:10]
        context['people'] = Character.objects.exclude(friends_by=user.id).exclude(username=user.username)
        context['follow'] = char.friends_by.filter(username=user.username)
        if user.username == char.username:
            context['follow'] = 'blank'  # позорище

        if user.is_authenticated and user.username == char.username:
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
        context['follow'] = char.friends_by.filter(username=user.username)
        if user.username == char.username:
            context['follow'] = 'blank'  # позорище
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


class HashView(ListView):
    model = HashtagList
    template_name = 'hashtag'


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
        writing.text = form.cleaned_data['blog_area']
        writing.save()

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
    return redirect(blog.get_absolute_url())


@login_required
@require_http_methods(["POST"])
def follow(request, username):
    user = auth.get_user(request)
    follower = Character.objects.get(username=username)
    user.friends.add(follower)
    return redirect('/')


def curry(_curried_func, *args, **kwargs):
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*(args + moreargs), **dict(kwargs, **morekwargs))
    return _curried

