# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.views.generic import TemplateView, ListView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from resources.models import Idc
from resources.forms import CreateIdcForm


# 机房列表
class IdcListView(LoginRequiredMixin, ListView):
    template_name = 'idc/idc_list.html'
    model = Idc
    paginate_by = 8
    ordering = 'id'

    def get_context_data(self, **kwargs):
        context = super(IdcListView, self).get_context_data(**kwargs)
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


# 创建机房
class IdcCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'idc/idc_create.html'

    def post(self, request):
        ret = {'status': 0}
        idc_form = CreateIdcForm(request.POST)
        if idc_form.is_valid():
            try:
                idc = Idc(**idc_form.cleaned_data)
                idc.save()
                ret['msg'] = '创建成功'
            except Exception:
                ret['status'] = 1
                ret['msg'] = '创建失败'
        else:
            ret['status'] = 1
            ret['msg'] = '创建失败'

        return JsonResponse(ret)


# 删除机房
class IdcDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        idc_id = request.POST.get('idc_id')
        try:
            Idc.objects.get(pk=idc_id).delete()
            ret['msg'] = '删除成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '删除失败'
        return JsonResponse(ret)


# 更新机房
class IdcModifyView(LoginRequiredMixin, TemplateView):
    template_name = 'idc/idc_modeify.html'

    def get_context_data(self, **kwargs):
        idc_id = self.request.GET.get('idc_id')
        context = super(IdcModifyView, self).get_context_data(**kwargs)
        context['idc_obj'] = Idc.objects.get(pk=idc_id)
        return context

    def post(self, request):
        ret = {'status': 0}
        idc_id = request.POST.get('idc_id')
        idc_form = CreateIdcForm(request.POST)
        if idc_form.is_valid():
            try:
                Idc.objects.filter(pk=idc_id).update(**idc_form.cleaned_data)
                ret['msg'] = '更新成功'
            except Exception:
                ret['status'] = 1
                ret['msg'] = '更新失败'
        else:
            ret['status'] = 1
            ret['msg'] = '更新失败'

        return JsonResponse(ret)