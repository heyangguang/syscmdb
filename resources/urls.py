# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.conf.urls import url, include

from resources.idc import views as idc_views
from resources.servers import views as server_views
from resources.serveruser import views as server_user_views

urlpatterns = [
    url(r'idc/', include([
        url(r'list/$', idc_views.IdcListView.as_view(), name='idc_list'),
        url(r'create/$', idc_views.IdcCreateView.as_view(), name='idc_create'),
        url(r'delete/$', idc_views.IdcDeleteView.as_view(), name='idc_delete'),
        url(r'modify/$', idc_views.IdcModifyView.as_view(), name='idc_modify'),
    ])),
    url(r'servers/', include([
        url(r'list/$', server_views.ServerListView.as_view(), name='server_list'),
        url(r'create/$', server_views.ServerCreateView.as_view(), name='server_create'),
        url(r'data_api/$', server_views.ServerDataApiView.as_view(), name='server_data_api'),
        url(r'detail/(?P<pk>\d+)/$', server_views.ServerDetailView.as_view(), name='server_detail'),
        url(r'modify_idc/$', server_views.ServerModifyIdcView.as_view(), name='server_modify_idc'),
        url(r'delete/$', server_views.ServerDeleteView.as_view(), name='server_delete'),
        url(r'flush/$', server_views.ServerFlushView.as_view(), name='server_flush'),
        url(r'get/$', server_views.ServerGetListView.as_view(), name='server_get'),
        url(r'set_product/$', server_views.ServerSetProduct.as_view(), name='server_set_product'),
    ])),
    url(r'serveruser/', include([
        url(r'list/$', server_user_views.ServerUserListView.as_view(), name='serveruser_list'),
        url(r'create/$', server_user_views.ServerUserCreateView.as_view(), name='serveruser_create'),
        url(r'modify/$', server_user_views.ServerUserModifyView.as_view(), name='serveruser_modify'),
        url(r'detail/(?P<pk>\d+)/$', server_user_views.ServerUserDetailView.as_view(), name='serveruser_detail'),
    ]))
]