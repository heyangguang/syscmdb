# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.conf.urls import url, include

from users import views
from users.user import views as user_views
from users.group import views as group_views
from users.perm import views as perm_views

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='user_logout'),
    url(r'^user/', include([
        url(r'list/$', user_views.UserListView.as_view(), name='user_list'),
        url(r'set_perm/$', user_views.UserSetPermView.as_view(), name='user_set_perm'),
        url(r'create/$', user_views.UserCreateView.as_view(), name='user_create'),
        url(r'delete/$', user_views.UserDeleteView.as_view(), name='user_delete'),
        url(r'stop/$', user_views.UserStopView.as_view(), name='user_stop'),
        url(r'start/$', user_views.UserStartView.as_view(), name='user_start'),
        url(r'modify/$', user_views.UserModifyView.as_view(), name='user_modify'),
        url(r'set_password/$', user_views.UserSetPasswordView.as_view(), name='user_set_password'),
        url(r'modify_group/$', user_views.UserModifyGroupView.as_view(), name='user_modify_group'),
        url(r'detail/(?P<pk>[0-9]+)/$', user_views.UserDetailView.as_view(), name='user_detail'),
        url(r'create_password/$', user_views.UserConfigPasswordView.as_view(), name='user_create_password'),
    ])),
    url(r'group/', include([
        url(r'list/$', group_views.GroupListView.as_view(), name='group_list'),
        url(r'create/$', group_views.GroupCreateView.as_view(), name='group_create'),
        url(r'delete/$', group_views.GroupDeleteView.as_view(), name='group_delete'),
        url(r'modify/$', group_views.GroupModifyView.as_view(), name='group_modify'),
        url(r'set_perm/$', group_views.GroupSetPermView.as_view(), name='group_set_perm'),
    ])),
    url(r'perm/', include([
        url(r'list/$', perm_views.PermListView.as_view(), name='perm_list'),
        url(r'create/$', perm_views.PermCreateView.as_view(), name='perm_create'),
        url(r'delete/$', perm_views.PermDeleteView.as_view(), name='perm_delete'),
    ])),
]