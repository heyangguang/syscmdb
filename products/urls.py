# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.conf.urls import url, include

from products import views

urlpatterns = [
    url(r'product/', include([
        url(r'list/$', views.ProductListApiView.as_view(), name='product_list'),
        url(r'modify/$', views.ProductModifyView.as_view(), name='product_modify'),
        url(r'create/$', views.ProductCreateView.as_view(), name='product_create'),
        url(r'get/$', views.ProductGetView.as_view(), name='product_get'),
        url(r'create_host/$', views.ProductCreateHostView.as_view(), name='product_create_host'),
    ]))
]