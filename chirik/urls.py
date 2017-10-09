"""chirik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404
from django.contrib import admin
from aas.views import IndexView, LogoutView, LoginView, RegView
from aas.views import UserView, UserEditView, BlogView, ArticlesView
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegView.as_view(), name='reg'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(?P<username>[-\w]+)/', include ('aas.urls')),
    #url(r'^(?P<username>\w+)/$', UserView.as_view(), name='user'),
    #url(r'^^(?P<username>\w+)/edit_user/$', UserEditView.as_view(), name='user_edit'),
    #url(r'^^(?P<username>\w+)/blog/$', BlogView.as_view(), name='blog'),
    #url(r'^^(?P<username>\w+)/blog/(?P<id>\d+)/$', ArticlesView.as_view(), name='comments'),
]
