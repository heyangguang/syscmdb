# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from users.forms import CreatePermForm


# 权限列表
class PermListView(LoginRequiredMixin, ListView):
    template_name = 'perm/perm_list.html'
    model = Permission
    ordering = 'id'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(PermListView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])
        return context

    def get_queryset(self):
        queryset = super(PermListView, self).get_queryset()
        queryset = queryset.exclude(name__regex='[a-zA-Z0-9]')
        return queryset

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        max_pages = page_obj.paginator.num_pages + 1

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


# 创建权限
class PermCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'perm/perm_create.html'

    def get_context_data(self, **kwargs):
        context = super(PermCreateView, self).get_context_data(**kwargs)
        context['model_list'] = ContentType.objects.all()
        return context

    def post(self, request):
        ret = {'status': 0}
        perm_form = CreatePermForm(request.POST)
        if perm_form.is_valid():
            perm = Permission(**perm_form.cleaned_data)
            try:
                perm.save()
                ret['msg'] = '添加成功'
                return JsonResponse(ret)
            except Exception as e:
                print(e.args)
                ret['status'] = 1
                ret['msg'] = '添加失败'
                return JsonResponse(ret)
        else:
            print(perm_form.errors)
            ret['status'] = 1
            ret['msg'] = '表单填写错误，添加失败'
            return JsonResponse(ret)


# 删除权限
class PermDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}

        perm_id = request.POST.get('perm_id', None)
        try:
            Permission.objects.get(pk=perm_id).delete()
            ret['msg'] = '删除成功'
        except Exception as e:
            ret['status'] = 1
            ret['msg'] = '删除失败, %s' %(e)

        return JsonResponse(ret)