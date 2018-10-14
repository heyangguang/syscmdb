from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# 登录用户
class UserLoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):

        ret = {'status': 0}

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            ret['next_url'] = request.GET.get('next') if request.GET.get('next', None) else '/'
        else:
            ret['status'] = 1
            ret['msg'] = '账号或密码错误，请联系管理员'

        return JsonResponse(ret)


# 注销用户
class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))