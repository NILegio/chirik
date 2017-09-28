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
from django.conf.urls import url, include
from django.contrib import admin
from aas.views import IndexView, UserView, LogoutView, UserEditView
from aas.form import LoginView, RegView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegView.as_view(), name='reg'),
    url(r'^logout/$', LogoutView.as_view(), name='logout' ),
    url(r'^(?P<pk>\d+)/$', UserView.as_view(), name='user'),
    url(r'^edit_user/(?P<pk>\d+)$', UserEditView.as_view(), name = 'user_edit')
]
