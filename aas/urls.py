from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from aas.views import UserView, UserEditView, ArticlesView, FriendsView, \
    add_comment, add_writing, FollowView #, follow

app_name = 'aas'

urlpatterns = [
    url(r'^$', UserView.as_view(), name='user'),
    #url(r'^follow/$', login_required(follow, login_url='login'), name='follow'),
    #url(r'^follow/$', follow, name='follow'),
    url(r'^follow/$', login_required(FollowView.as_view(), login_url='login'), name='follow'),
    #url(r'^friends/$', FriendsView.as_view(), name='friends'),
    url(r'^edit_user/$', UserEditView.as_view(), name='user_edit'),
    url(r'^blog/add/$', add_writing, name='add_writer'),
    url(r'^blog/(?P<id>\d+)/$', ArticlesView.as_view(), name='comments'),
    url(r'^blog/comment/(?P<id>\d+)/$', add_comment, name='add_comment'),
    ]
