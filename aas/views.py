from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Character, Blog, Commentary, HashtagList
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template import RequestContext
from aas.form import BlogForm, CommentForm
from django.template.context_processors import csrf

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class UserView(DetailView): # deatail
    template_name = 'user.html'
    model = Character

    def get_object(self):
        idi = self.model.objects.get(username=self.kwargs['username'])
        return self.model.objects.get(pk = idi.pk)


class UserEditView(UpdateView):
    template_name = 'edit_user.html'
    model = Character
    fields = ('first_name', 'last_name',)

    def get_object(self):
        idi = self.model.objects.get(username=self.kwargs['username'])
        return self.model.objects.get(pk = idi.pk)

    def get_success_url(self):
        return reverse_lazy('aas:user', args = [str(self.kwargs['username'])])


class BlogView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        char = get_object_or_404(Character, username=self.kwargs['username'])
        context['blog_list'] = char.blog.all().order_by('pub_date')
        return context


class ArticlesView(TemplateView):
    template_name = 'comments.html'
    comment_form = CommentForm

    def get(self, request, *args, **kwargs):
        context = {}
        blog = get_object_or_404(Blog, id=self.kwargs['id'])
        context.update(csrf(self.request))
        user = auth.get_user(self.request)
        context['comments'] = blog.commentary.all().order_by('pub_date')
        context['next'] = blog.get_absolute_url()
        if user.is_authenticated:
            context['form'] = self.comment_form

        return context


@login_required
@require_http_methods
def add_comments(request, blog_id):

    form = CommentForm(request.POST)
    blog = get_object_or_404(Blog, id=blog_id)

    if form.is_valid():
        comment = Commentary()
        comment.blog = blog
        comment.owner = auth.get_user(request)
        comment.text = form.cleaned_data['comment_area']
        comment.save()

    return redirect(blog.get_absolute_url())


class HashView(ListView):
    model = HashtagList
    template_name = 'hashtag'


class FriendsView(ListView):
    pass


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
