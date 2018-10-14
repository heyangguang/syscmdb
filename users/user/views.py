# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View, DetailView
from django.http import HttpResponse, JsonResponse
from users.models import Profile
from django.contrib.auth.models import Group, User, Permission
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.forms.models import model_to_dict

from users.forms import CreateUserForm, CreateProfileForm
from users.models import Profile, RegisterEmail

from utils.sendmail import send_mail
from utils.password_url_hash import random_str


# 用户列表
class UserListView(LoginRequiredMixin, ListView):
    template_name = 'user/user_list.html'
    model = Profile
    paginate_by = 5
    ordering = 'id'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

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


# 创建用户
class UserCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_create.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()

        return context

    def post(self, request):
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)

        print('表单提交失败')
        print(user_form.errors)
        print(profile_form.errors)

        if user_form.is_valid() and profile_form.is_valid():

            user = User(**user_form.cleaned_data)
            user.save()
            print('User表OK,,,,')

            user_profile = Profile()
            user_profile.user = user
            user_profile.name = profile_form.cleaned_data['name']
            user_profile.lnvalid_date = profile_form.cleaned_data['lnvalid_date']
            user_profile.phone = profile_form.cleaned_data['phone']
            user_profile.weixin = profile_form.cleaned_data['weixin']
            user_profile.info = request.POST.getlist('info', None)[0]
            user_profile.save()

            print('userprofile表OK,,,,')

            if request.POST.get('groups', None):
                user.groups.set(request.POST.getlist('groups'))

            register_email = RegisterEmail()
            register_email.user = user
            register_email.type_code = 0
            register_email.code = random_str()
            register_email.save()

            contnet = """
            <p>你好 %s: </p>
            
            <p>恭喜您，您的账号已经创建成功 </p>

            <p>用户名: %s </p>

            <p><a href='%s'>请点击这里设置密码</a> </p>
            """ %(user.username, user_profile.name, settings.HOST_URL + reverse('user_create_password') + '?code=' + str(register_email.code))

            try:
                send_mail(settings.EMAIL_USER, settings.EMAIL_PASSWORD, user.email,
                          settings.EMAIL_TITLE, contnet, settings.EMAIL_HOST, settings.EMAIL_PORT)
                print('邮件发送OK...')
            except:
                print('邮件发送失败...')

        return redirect(reverse('user_list'))


# 设置密码
class UserConfigPasswordView(TemplateView):
    template_name = 'user/user_config_passwd.html'

    def get_context_data(self, **kwargs):
        context = super(UserConfigPasswordView, self).get_context_data(**kwargs)

        code = self.request.GET.get('code', None)

        try:
            register_email_obj = RegisterEmail.objects.get(code=code)
            context['user_obj'] = register_email_obj.user
            context['code'] = code
        except User.DoesNotExist:
            pass

        return context

    def post(self, request):
        ret = {"status": 0}

        code = request.POST.get('code')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        print(request.POST)

        if password_1 == password_2:
            try:
                register_email_obj = RegisterEmail.objects.get(code=code)
                if register_email_obj.active_status == 0:
                    register_email_obj.user.set_password(password_1)
                    register_email_obj.user.save()
                    register_email_obj.active_status = 1
                    register_email_obj.save()
                    ret['msg'] = '设置密码成功,点击OK后自动跳转登录页'
                else:
                    ret['status'] = 1
                    ret['msg'] = '激活码异常，请联系管理员'
            except User.DoesNotExist:
                ret['status'] = 1
                ret['msg'] = '没有此用户'
            except Exception:
                ret['status'] = 1
                ret['msg'] = '异常错误，请练习管理员'
        else:
            ret['status'] = 1
            ret['msg'] = '两次密码输入不一样，请重新输入'
        return JsonResponse(ret)


# 删除用户
class UserDeleteView(View):

    def post(self, request):
        ret = {'status': 0}
        uid = request.POST.get('user_id', None)

        try:
            User.objects.get(id=uid).delete()
            ret['msg'] = '删除用户成功'
        except User.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '此用户不存在，删除失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 禁用用户
class UserStopView(View):

    def post(self, request):
        ret = {'status': 0}
        uid = request.POST.get('user_id', None)

        try:
            user = User.objects.get(id=uid)
            user.is_active=False
            user.save()

            ret['msg'] = '禁用%s用户成功' %(user.username)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '此用户不存在，禁用失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 启动用户
class UserStartView(View):

    def post(self, request):
        ret = {'status': 0}
        uid = request.POST.get('user_id', None)

        try:
            user = User.objects.get(id=uid)
            user.is_active=True
            user.save()

            ret['msg'] = '启用%s用户成功' %(user.username)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '此用户不存在，启用失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 修改用户
class UserModifyView(View):

    def get(self, request):
        uid = request.GET.get('uid', None)
        user_obj = User.objects.get(id=uid)
        groups = Group.objects.all()
        print(groups)

        return render(request, 'user/user_modify.html', {"user": user_obj, "groups": groups})

    def post(self, request):
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        uid = request.POST.get('uid', None)
        user = User.objects.get(pk=uid)
        groups = Group.objects.all()

        if user_form.is_valid() and profile_form.is_valid():
            print(user_form.cleaned_data)
            user.username=user_form.cleaned_data['username']
            user.email=user_form.cleaned_data['email']
            user.is_superuser=user_form.cleaned_data['is_superuser']
            user.save()

            print('用户表更新完成OK...')

            profile = Profile.objects.filter(user=user)

            profile.update(
                name=profile_form.cleaned_data['name'],
                lnvalid_date=profile_form.cleaned_data['lnvalid_date'],
                phone=profile_form.cleaned_data['phone'],
                weixin=profile_form.cleaned_data['weixin'],
                info=request.POST.getlist('info', None)[0]
            )
            print('Profile表更新完成OK...')

            if request.POST.getlist('groups', None):
                user.groups.set(request.POST.getlist('groups'))
            else:
                user.groups.clear()
            print('用户组更新完成OK....')

        return render(request, 'user/user_modify.html', {"user": user, "groups": groups})


# 查看用户
class UserDetailView(DetailView):
    template_name = 'user/user_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        context['groups'] = Group.objects.all()
        return context


# 修改用户的用户组
class UserModifyGroupView(View):

    def post(self, request):
        ret = {"status": 0, 'msg': '修改成功'}
        groups = request.POST.getlist('groups[]', None)
        uid = request.POST.get('uid', None)
        print(request.POST)
        print(uid)

        try:
            user = User.objects.get(pk=uid)
            if groups:
                try:
                    user.groups.set(groups)
                except Exception:
                    ret['status'] = 1
                    ret['msg'] = '其他错误，修改失败请联系管理员'
            else:
                user.groups.clear()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['msg'] = '没有此用户，修改失败'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '其他错误，请联系系统管理员'

        return JsonResponse(ret)


# 管理员设置密码
class UserSetPasswordView(View):

    def post(self, request):
        ret = {"status":0}

        password_1 = request.POST.get('password_1', None)
        password_2 = request.POST.get('password_2', None)
        uid = request.POST.get('uid', None)

        if password_1 and password_2:
            if password_1 == password_2:
                try:
                    user = User.objects.get(pk=uid)
                    user.set_password(password_1)
                    user.save()
                    ret['msg'] = '设置密码成功'
                except User.DoesNotExist:
                    ret['status'] = 1
                    ret['msg'] = '此用户不存在，设置失败'
                except Exception:
                    ret['status'] = 1
                    ret['msg'] = '其他错误，设置失败，请联系系统管理员'
            else:
                ret['status'] = 1
                ret['msg'] = '密码不一致，设置失败'
        else:
            ret['status'] = 1
            ret['msg'] = '空密码设置失败'

        return JsonResponse(ret)


# 设置用户权限
class UserSetPermView(TemplateView):
    template_name = 'user/user_set_perm.html'

    def get_context_data(self, **kwargs):
        uid = self.request.GET.get('uid')
        context = super(UserSetPermView, self).get_context_data(**kwargs)
        context['perm_list'] = Permission.objects.all()
        context['user_obj'] = User.objects.get(pk=uid)

        return context

    def post(self, request):
        ret = {'status': 0}

        uid = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=uid)
            user.user_permissions = request.POST.getlist('perm_list[]')
            user.save()
            ret['msg'] = '设置成功'
        except Exception:
            ret['status'] = 1
            ret['msg'] = '设置失败'

        return JsonResponse(ret)