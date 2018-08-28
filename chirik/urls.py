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
from django.views.static import serve
from django.conf import settings
from django.views.defaults import server_error, page_not_found

from aas.views import IndexView, LogoutView, LoginView, RegView, HashView, curry

handler404 = curry(page_not_found, exception=Exception('Page not Found'), template_name='errors/error404.html')
handler500 = curry(server_error, template_name='errors/error500.html')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegView.as_view(), name='reg'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^hashtag/(?P<hashtag>\w+)/$', HashView.as_view(), name='hashtag'),

    url(r'^(?P<username>[-\w]+)/', include('aas.urls')),
]

