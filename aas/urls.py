from django.conf.urls import url
from aas.views import UserView, UserEditView, BlogView, ArticlesView, add_comment, add_writing

app_name = 'aas'
urlpatterns = [
    url(r'^$', UserView.as_view(), name='user'),
    url(r'^edit_user/$', UserEditView.as_view(), name='user_edit'),
    url(r'^blog/$', BlogView.as_view(), name='blog'),
    url(r'^blog/add/$', add_writing, name='add_writer'),
    url(r'^blog/(?P<id>\d+)/$', ArticlesView.as_view(), name='comments'),
    url(r'^blog/comment/(?P<id>\d+)/$', add_comment, name='add_comment'),
    ]
