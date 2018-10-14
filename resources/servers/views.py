# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from resources.models import Server, ServerAuto

import json


class ServerListView(ListView):
    template_name = 'servers/server_list.html'
    model = Server

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context['os_list'] = ServerAuto.os_status_list
        context['system_list'] = ServerAuto.system_status_list
        return context


# 自动推送服务器脚本
class ServerCreateView(View):

    def post(self, request):
        ret = {'status': 0}
        print(request.POST)
        return JsonResponse(ret)


# 接收服务器数据接口
class ServerDataApiView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {'status': 0}
        print(request.POST)
        print(request.POST.get('cpu_info'))
        return JsonResponse(ret)