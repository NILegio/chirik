from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.template.context_processors import csrf
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy, reverse
from .models import Character, Blog, Commentary, HashtagList
from aas.form import BlogForm, CommentForm, MyUserChangeForm, MyUserCreationForm


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class UserView(DetailView):
    template_name = 'user.html'
    model = Character
    blog_form = BlogForm

    def get_object(self):
        idi = self.model.objects.get(username=self.kwargs['username'])
        return self.model.objects.get(pk = idi.pk)

    def get_context_data(self, **kwargs):

        context = super(DetailView, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['blogs'] = char.blog.all().order_by('pub_date')
        if user.is_authenticated:
            context['form'] = self.blog_form
        return context


class UserEditView(UpdateView):
    template_name = 'edit_user.html'
    model = Character
    fields = ('first_name', 'last_name',)

    def get_object(self):
        idi = self.model.objects.get(username=self.kwargs['username'])
        return self.model.objects.get(pk=idi.pk)

    def get_success_url(self):
        return reverse_lazy('aas:user', args=[str(self.kwargs['username'])])
        #return reverse_lazy('user', args=[str(self.kwargs['username'])])


class BlogView(TemplateView):
    template_name = 'blog.html'
    blog_form = BlogForm

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['blogs'] = char.blog.all().order_by('pub_date')
        if user.is_authenticated:
            context['form'] = self.blog_form
        return context


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





class ArticlesView(TemplateView):

    template_name = 'comments.html'
    comment_form = CommentForm

    def get_context_data(self, **kwargs):
        blog = get_object_or_404(Blog, id=kwargs['id'])
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        context['blog'] = blog
        context['comments'] = blog.commentary.all().order_by('path')
        context['next'] = blog.get_absolute_url()
        if user.is_authenticated:
            context['form'] = self.comment_form
        return context

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

#    try:
#        comment.path.extend(Commentary.objects.get(id=form.cleaned_data['parent_comment']).path)
#        comment.path.append(comment.id)
#    except ObjectDoesNotExist:
#        comment.path.append(comment.id)

#    comment.save()

    return redirect(blog.get_absolute_url())


class HashView(ListView):
    model = HashtagList
    template_name = 'hashtag'


class FriendsView(ListView):

    pass


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
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
