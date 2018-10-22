from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product


# Create your views here.


# 业务线列表API
class ProductListApiView(LoginRequiredMixin, TemplateView):
    template_name = 'products/products_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListApiView, self).get_context_data(**kwargs)
        ztree = ProductTree().get()
        context['ztree'] = ztree
        context['users'] = User.objects.all()
        return context

    def post(self, request):
        ret = {'status': 0}
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            ret['product_name'] = product.name
            ret['product_name_cn'] = product.name_cn
            try:
                ret['product_pname'] = Product.objects.get(pk=product.pid).name_cn
            except Exception:
                ret['product_pname'] = '无'
            ret['op_interface'] = product.op_interface
            ret['dev_interface'] = product.dev_interface
        except Exception:
            ret['status'] = 1
            ret['msg'] = '获取数据失败'

        return JsonResponse(ret)


# 更改业务线
class ProductModifyView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {'status': 0}
        try:
            Product.objects.filter(id=request.POST.get('id')).update(
                name=request.POST.get('name'),
                name_cn=request.POST.get('name_cn'),
                dev_interface=",".join(request.POST.getlist('dev_interface[]')),
                op_interface=",".join(request.POST.getlist('op_interface[]'))
            )
            ret['msg'] = '修改成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '修改失败'

        return JsonResponse(ret)


# 创建业务线
class ProductCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product_create.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['p_list'] = Product.objects.all().exclude(level=3)
        context['user_list'] = User.objects.all().exclude(is_superuser=1)
        print(context['user_list'])
        return context

    def post(self, request):
        ret = {'status': 0}
        pid = request.POST.get('pid')
        try:
            Product.objects.create(
                name=request.POST.get('name'),
                name_cn=request.POST.get('name_cn'),
                dev_interface=','.join(request.POST.getlist('dev_interface')),
                op_interface=','.join(request.POST.getlist('op_interface')),
                pid=pid,
                level=1 if int(pid)==0 else 2
            )
            ret['msg'] = '创建成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '创建失败'
        return JsonResponse(ret)


# 创建机器组
class ProductCreateHostView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product_host_create.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateHostView, self).get_context_data(**kwargs)
        context['p_list'] = Product.objects.filter(level=2)
        context['user_list'] = User.objects.all().exclude(is_superuser=1)
        print(context['user_list'])
        return context

    def post(self, request):
        ret = {'status': 0}
        pid = request.POST.get('pid')
        try:
            Product.objects.create(
                name=request.POST.get('name'),
                name_cn=request.POST.get('name_cn'),
                dev_interface=','.join(request.POST.getlist('dev_interface')),
                op_interface=','.join(request.POST.getlist('op_interface')),
                pid=pid,
                level=3
            )
            ret['msg'] = '创建成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '创建失败'
        return JsonResponse(ret)


# 获取product信息
class ProductGetView(LoginRequiredMixin, View):

    def get(self, request):
        ret = {'status': 0}
        product_id = request.GET.get('product_id')
        data = Product.objects.filter(pid=product_id).values('id', 'name_cn')
        ret['data'] = list(data)
        return JsonResponse(ret)


# 项目数展示
class ProductTree(object):

    def __init__(self):
        self.data = self.get_all_product()

    def get_all_product(self):
        return Product.objects.all()

    def get(self):
        ret = []
        for product in self.data.filter(pid=0):
            node = self.get_node(product)
            node['children'] = self.get_children(product.id)
            ret.append(node)
        return ret

    def get_children(self, product_id):
        ret = []
        for product in self.data.filter(pid=product_id):
            node = self.get_node(product)
            node['children'] = self.get_not_children(product.id)
            ret.append(node)
        return ret

    def get_not_children(self, product_id):
        ret = []
        for product in self.data.filter(pid=product_id):
            node = self.get_node(product)
            ret.append(node)
        return ret

    def get_node(self, product):
        ret = {
            'text': product.name_cn,
            'id': product.id,
            'level': product.level,
        }
        return ret

