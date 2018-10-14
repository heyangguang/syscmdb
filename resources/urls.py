# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.conf.urls import url, include

from resources.idc import views as idc_views
from resources.servers import views as server_views

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
    ]))
]