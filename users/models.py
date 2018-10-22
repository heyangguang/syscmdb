from django.db import models
from django.contrib.auth.models import User, Group, Permission

from datetime import datetime


# Create your models here.


# 用户表扩展
class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=10, verbose_name='中文名')
    phone = models.CharField(max_length=11, verbose_name='电话')
    weixin = models.CharField(max_length=32, verbose_name='微信')
    info = models.TextField(verbose_name='备注')
    lnvalid_date = models.CharField(max_length=32, verbose_name='失效日期')

    class Meta:
        default_permissions = []
        permissions = (
            ('add_user', '添加用户'),
            ('delete_user', '删除用户'),
            ('view_user', '查看用户'),
            ('modify_user', '修改用户'),
            ('user_status_stop', '禁止或允许用户'),
            ('user_set_password', '禁止用户密码'),
            ('user_set_perm', '设置用户权限'),
        )


# 邮件激活，邮件找回，密码表
class RegisterEmail(models.Model):
    type_list = [
        (0, '注册密码'),
        (1, '找回密码'),
    ]
    type_code = models.IntegerField(choices=type_list, verbose_name='验证码类型')
    code = models.CharField(max_length=50, verbose_name='验证码')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    active_status = models.BooleanField(default=0, verbose_name='激活状态')
    user = models.ForeignKey(User)

    class Meta:
        default_permissions = []


# 用户组表扩展
class GroupProfile(models.Model):
    group = models.OneToOneField(Group)
    info = models.TextField(verbose_name='备注')

    class Meta:
        default_permissions = []
        permissions = (
            ('add_group', '添加用户组'),
            ('delete_group', '删除用户组'),
            ('view_group', '查看用户组'),
            ('modify_group', '修改用户组'),
            ('group_set_perm', '设置用户组权限'),
        )

# ('add_perm', '添加权限'),
# ('delete_perm', '删除权限'),
# ('view_perm', '查看权限'),
