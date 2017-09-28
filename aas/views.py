from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.base import View
from django.contrib.auth import login, logout
from .models import Character, Blog, Commentary, HashtagList
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class UserView(DetailView): # deatail
    template_name = 'user.html'
    model = Character


class UserEditView(UpdateView):
    template_name = 'edit_user.html'
    model = Character
    fields = ('first_name', 'last_name',)

    def get_success_url(self):
        return reverse_lazy('user', args = (self.kwargs['pk']))


class BlogView(View): #formview
    pass

class HashView(ListView):
    model = HashtagList
    template_name = 'hashtag'

class FriendsView(ListView):
    pass

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')






