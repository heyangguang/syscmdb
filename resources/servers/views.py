# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.views.generic import ListView, View, DetailView, TemplateView
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin

from resources.models import Server, ServerAuto, Disk, Ip, Idc, ServerUser
from resources.forms import CreateServerAutoForm, CreateServerForm
from utils.upload import sftp_upload_file
from utils.exec_comd import sftp_exec_command
from products.models import Product

import json


# 服务器展示
class ServerListView(LoginRequiredMixin, ListView):
    template_name = 'servers/server_list.html'
    model = Server

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context['os_list'] = ServerAuto.os_status_list
        context['system_list'] = ServerAuto.system_status_list
        context['systemuser_list'] = ServerUser.objects.all()
        return context


# 自动推送服务器脚本
class ServerCreateView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        server_auto_form = CreateServerAutoForm(request.POST)
        serveruser_id = request.POST.get('serveruser_id')
        serveruser = ServerUser.objects.get(pk=serveruser_id)
        if server_auto_form.is_valid():
            server_auto = ServerAuto(**server_auto_form.cleaned_data)
            try:
                ret_sftp_status = sftp_upload_file(server_auto.ip_inner, serveruser.username, serveruser.password,
                                                   '/tmp/scan_systeminfo.py',
                                                   '/tmp/syscmdb/utils/scan_systeminfo.py')
                if ret_sftp_status['status'] == 0:
                    server_auto.save()
                    ret_commd_status = sftp_exec_command(server_auto.ip_inner, server_auto.port, serveruser.username,
                                                         serveruser.password,
                                                         '/usr/bin/python /tmp/scan_systeminfo.py %s %s' % (
                                                             server_auto.id, '0'))
                    if ret_commd_status['status'] == 0:
                        ret['msg'] = '自动推送完成'
                    else:
                        server_auto.delete()
                        ret = ret_commd_status
                else:
                    ret = ret_sftp_status
            except Exception as e:
                ret['status'] = 1
                ret['msg'] = '上传失败 %s' % e
        else:
            ret['status'] = 1
            ret['msg'] = '推送失败'
        return JsonResponse(ret)


# 接收服务器数据接口
class ServerDataApiView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {'status': 0}
        data = request.body
        data_dict = json.loads(data)
        server_form = CreateServerForm(data_dict)
        print(data_dict)
        if server_form.is_valid():
            try:
                server = Server(**server_form.cleaned_data)
                server.server_auto_id = data_dict['server_auto_id']
                server.scan_status = 1
                server.save()

                for key, value in data_dict['disk_info'].items():
                    Disk.objects.create(name=key, size=value, server=server)

                for key, value in data_dict['ip_info'].items():
                    Ip.objects.create(name=key, ip_address=value, server=server)
            except:
                ret['status'] = 1
                ret['msg'] = '添加服务器失败'
        return JsonResponse(ret)

    def put(self, request):
        ret = {'status': 0}
        data = request.body
        data_dict = json.loads(data)
        server_auto_id = data_dict['server_auto_id']
        server_id = ServerAuto.objects.get(pk=server_auto_id).server.id
        print(server_id)
        server_form = CreateServerForm(data_dict)
        print('put', data_dict)
        if server_form.is_valid():
            try:
                server = Server.objects.get(pk=server_id)
                server.hostname = server_form.cleaned_data['hostname']
                server.cpu_info = server_form.cleaned_data['cpu_info']
                server.cpu_count = server_form.cleaned_data['cpu_count']
                server.mem_info = server_form.cleaned_data['mem_info']
                server.os_system = server_form.cleaned_data['os_system']
                server.os_system_num = server_form.cleaned_data['os_system_num']
                server.save()

                server.disk_set.all().delete()
                server.ip_set.all().delete()

                for key, value in data_dict['disk_info'].items():
                    Disk.objects.create(name=key, size=value, server=server)

                for key, value in data_dict['ip_info'].items():
                    Ip.objects.create(name=key, ip_address=value, server=server)

            except:
                ret['status'] = 1
                ret['msg'] = '添加服务器失败'
        return JsonResponse(ret)


# 服务器详情展示
class ServerDetailView(LoginRequiredMixin, DetailView):
    template_name = 'servers/server_detail.html'
    model = Server

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)
        context['idc_list'] = Idc.objects.all()
        return context


# 修改服务器的IDC机房归属
class ServerModifyIdcView(LoginRequiredMixin, View):

    def post(self, request):
        print(request.POST)
        ret = {"status": 0, 'msg': '修改成功'}
        idc_id = request.POST.get('idc_id')
        server_id = request.POST.get('server_id')
        try:
            server = Server.objects.get(pk=server_id)
            if idc_id:
                try:
                    server.idcs_id = idc_id
                    server.save()
                except Exception:
                    ret['status'] = 1
                    ret['msg'] = '其他错误，修改失败请联系管理员'
            else:
                server.idcs = None
        except Server.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '没有此服务器，修改失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 删除服务器
class ServerDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        server_id = request.POST.get('server_id')

        try:
            server = Server.objects.get(id=server_id)
            server.server_auto.delete()
            server.delete()
            ret['msg'] = '删除服务器成功'
        except Server.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '此服务器不存在，删除失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 刷新探测服务器
class ServerFlushView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        server_id = request.POST.get('server_id')
        try:
            server = Server.objects.get(pk=server_id)
            try:
                ret_sftp_status = sftp_upload_file(server.server_auto.ip_inner, server.server_user.username,
                                                   server.server_user.password,
                                                   '/tmp/scan_systeminfo.py',
                                                   '/tmp/syscmdb/utils/scan_systeminfo.py')
                if ret_sftp_status['status'] == 0:
                    ret_commd_status = sftp_exec_command(server.server_auto.ip_inner, server.server_auto.port,
                                                         server.server_user.username,
                                                         server.server_user.password,
                                                         '/usr/bin/python /tmp/scan_systeminfo.py %s %s' % (
                                                             server.server_auto.id, '1'))
                    if ret_commd_status['status'] == 0:
                        server.scan_status = 1
                        server.save()
                        ret['msg'] = '刷新探测完成'
                    else:
                        server.scan_status = 0
                        server.save()
                        ret = ret_commd_status
                else:
                    server.scan_status = 0
                    server.save()
                    ret = ret_sftp_status
            except Exception as e:
                if server.server_user:
                    server.scan_status = 0
                    server.save()
                    ret['status'] = 1
                    ret['msg'] = '上传失败 %s' % e
                else:
                    server.scan_status = 0
                    server.save()
                    ret['status'] = 1
                    ret['msg'] = '上传失败,没关联资产用户'
        except Server.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '刷新失败，主机不存在'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '刷新失败'
        return JsonResponse(ret)


# 业务线获取主机信息
class ServerGetListView(LoginRequiredMixin, View):

    def get(self, request):
        ret = {'status': 0}
        product_id = request.GET.get('id')
        try:
            product = Product.objects.get(pk=product_id)
            ret['data'] = list(
                product.product_host.all().values('id', 'hostname', 'server_auto__ip_inner', 'scan_status',
                                                  'idcs__name_cn'))
        except Exception:
            ret['status'] = 1
            ret['msg'] = '查询失败'
        return JsonResponse(ret)


# 设置业务线
class ServerSetProduct(LoginRequiredMixin, TemplateView):
    template_name = 'servers/server_set_product.html'

    def get_context_data(self, **kwargs):
        context = super(ServerSetProduct, self).get_context_data(**kwargs)
        server_id = self.request.GET.get('id')
        server = Server.objects.get(pk=server_id)
        context['server'] = server
        context['product_one_list'] = Product.objects.filter(level=1)
        context['product_two_list'] = Product.objects.filter(level=2)
        context['product_host_list'] = Product.objects.filter(level=3)
        return context

    def post(self, request):
        ret = {'status': 0}
        server_id = request.POST.get('server_id')
        product_one = request.POST.get('product_one')
        product_two = request.POST.get('product_two')
        product_host = request.POST.get('product_host')
        if product_one and product_two and product_host:
            try:
                Server.objects.filter(pk=server_id).update(
                    product_one=product_one,
                    product_two=product_two,
                    product_host=product_host,
                )
                ret['msg'] = '设置成功'
            except Exception:
                ret['status'] = 1
                ret['msg'] = '设置失败'
        else:
            ret['status'] = 1
            ret['msg'] = '设置失败'
        return JsonResponse(ret)
