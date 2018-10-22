from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from resources.models import Server, Product
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_count'] = User.objects.all().count()
        context['group_count'] = Group.objects.all().count()
        context['host_count'] = Server.objects.all().count()
        context['host_error_count'] = Server.objects.filter(scan_status=0).count()
        context['server_list'] = Server.objects.all().order_by('-update_date')
        context['productd_count'] = Product.objects.filter(level=1).count()
        return context

