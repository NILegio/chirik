from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.contrib.auth import login, logout
from .models import Character, Blog, Commentary, HashtagList
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template import RequestContext

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
        return reverse_lazy('user', args = [str(self.kwargs['username'])])


class BlogView(View): #formview
    template_name = 'blog.html'


class HashView(ListView):
    model = HashtagList
    template_name = 'hashtag'

class FriendsView(ListView):
    pass

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')

def e_handler404(request):
    context = RequestContext(request)
    responce = render_to_response('error/error404.html', context)
    responce.status_code = 404
    return responce

def e_handler500(request):
    context = RequestContext(request)
    responce = render_to_response('error/error500.html', context)
    responce.status_code = 500
    return responce








