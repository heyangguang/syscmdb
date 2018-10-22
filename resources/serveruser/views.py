# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.views.generic import TemplateView, ListView, DetailView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from resources.models import ServerUser, Server


# 主机资源用户展示
class ServerUserListView(LoginRequiredMixin, ListView):
    template_name = 'serveruser/serveruser_list.html'
    model = ServerUser


# 主机资源用户创建
class ServerUserCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'serveruser/serveruser_create.html'

    def get_context_data(self, **kwargs):
        context = super(ServerUserCreateView, self).get_context_data(**kwargs)
        context['server_list'] = Server.objects.filter(server_user=None)
        return context

    def post(self, request):
        ret = {'status': 0}
        try:
            server_user = ServerUser.objects.create(
                name=request.POST.get('name'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                info=request.POST.get('info'),
            )
            serveruser_list = request.POST.getlist('serveruser_id')
            for server_id in serveruser_list:
                server = Server.objects.get(pk=server_id)
                server.server_user = server_user
                server.save()
            ret['msg'] = '创建成功'
        except Exception as e:
            print(e)
            ret['status'] = 1
            ret['msg'] = '创建失败'

        return JsonResponse(ret)


# 主机资源用户详情信息
class ServerUserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'serveruser/serveruser_detail.html'
    model = ServerUser

    def get_context_data(self, **kwargs):
        context = super(ServerUserDetailView, self).get_context_data(**kwargs)
        context['server_list'] = Server.objects.all()
        return context


# 主机资源用户修改
class ServerUserModifyView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        try:
            serveruser_id = request.POST.get('serveruser_id')
            password = request.POST.get('password')
            server_id_list = request.POST.getlist('server_id')
            if password:
                ServerUser.objects.filter(pk=serveruser_id).update(
                    name=request.POST.get('name'),
                    username=request.POST.get('username'),
                    password=password,
                    info=request.POST.get('info'),
                )
            else:
                ServerUser.objects.filter(pk=serveruser_id).update(
                    name=request.POST.get('name'),
                    username=request.POST.get('username'),
                    info=request.POST.get('info'),
                )
            serveruser = ServerUser.objects.get(pk=serveruser_id)
            serveruser.server_set.clear()
            for server_id in server_id_list:
                server = Server.objects.get(pk=server_id)
                server.server_user_id = serveruser_id
                server.save()
            ret['msg'] = '修改成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '修改失败'
        return JsonResponse(ret)