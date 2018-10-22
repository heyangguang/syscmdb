# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.views.generic import ListView, TemplateView, View
from users.models import GroupProfile
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin


# 用户组列表
class GroupListView(LoginRequiredMixin, ListView):
    template_name = 'group/group_list.html'
    model = GroupProfile
    paginate_by = 8
    ordering = 'id'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)

        context['page_range'] = self.get_pagerange(context['page_obj'])
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        max_pages = page_obj.paginator.num_pages + 1
        print(max_pages)

        start = current_index - 1
        end = current_index + 2

        if end > max_pages:
            start = start - 1
            end = max_pages

        if start < 1:
            if end < max_pages:
                end = end + 1
            start = 1

        return range(start, end)


# 创建用户组
class GroupCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'group/group_create.html'

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        return context

    def post(self, request):
        print(request.POST)

        group = Group()
        group.name = request.POST.get('name')
        group.save()

        group_profile = GroupProfile()
        group_profile.group = group
        group_profile.info = request.POST.get('info')
        group_profile.save()

        for user_id in request.POST.getlist('users'):
            User.objects.get(pk=user_id).groups.add(group)

        print('用户组oK...')
        return redirect(reverse('group_list'))


# 删除用户组
class GroupDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        gid = request.POST.get('group_id', None)

        try:
            Group.objects.get(id=gid).delete()
            ret['msg'] = '删除用户组成功'
        except User.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '此用户组不存在，删除失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 更新用户组
class GroupModifyView(LoginRequiredMixin, TemplateView):
    template_name = 'group/group_modify.html'

    def get_context_data(self, **kwargs):
        gid = self.request.GET.get('gid')

        context = super(GroupModifyView, self).get_context_data(**kwargs)
        context['user_list'] = User.objects.all()
        context['group_obj'] = Group.objects.get(pk=gid)
        context['gid'] = gid

        return context

    def post(self, request):
        print(request.POST)

        group_name = request.POST.get('name')
        users = request.POST.getlist('users')
        info = request.POST.get('info')
        gid = request.POST.get('gid')

        group_obj = Group.objects.get(pk=gid)
        group_obj.name = group_name
        group_obj.groupprofile.info = info
        group_obj.save()
        group_obj.groupprofile.save()
        for user_id in users:
            group_obj.user_set.add(User.objects.get(pk=user_id))


        return render(request, 'group/group_modify.html',
                      {'gid': gid, 'group_obj': group_obj, 'user_list': User.objects.all()})


# 用户组设置权限
class GroupSetPermView(LoginRequiredMixin, TemplateView):
    template_name = 'group/group_set_perm.html'

    def get_context_data(self, **kwargs):
        gid = self.request.GET.get('gid')
        context = super(GroupSetPermView, self).get_context_data(**kwargs)
        context['group_obj'] = Group.objects.get(pk=gid)
        context['perm_list'] = Permission.objects.all().exclude(name__regex='[a-zA-Z0-9]')

        return context

    def post(self, request):
        ret = {'status': 0}
        print(request.POST)

        gid = request.POST.get('group_id')
        try:
            group = Group.objects.get(pk=gid)
            group.permissions.set(request.POST.getlist('perm_list[]'))
            ret['msg'] = '设置成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '设置失败'

        return JsonResponse(ret)

