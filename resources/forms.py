# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django import forms


# 创建IDC表单
class CreateIdcForm(forms.Form):
    name = forms.CharField(required=True, max_length=10)
    name_cn = forms.CharField(required=True, max_length=32)
    address = forms.CharField(max_length=64, required=False)
    username = forms.CharField(max_length=32, required=True)
    username_phone = forms.CharField(max_length=32, required=True)
    phone = forms.CharField(max_length=32, required=True)
    email = forms.EmailField(required=True)


# 服务器接口表单
class CreateServerForm(forms.Form):
    hostname = forms.CharField(required=True, max_length=64)
    cpu_info = forms.CharField(required=True, max_length=64)
    cpu_count = forms.IntegerField(required=True)
    mem_info = forms.CharField(required=True, max_length=32)
    os_system = forms.CharField(required=True, max_length=32)
    os_system_num = forms.IntegerField(required=True)
    uuid = forms.CharField(required=True, max_length=64)
    sn = forms.CharField(required=True, max_length=64)
    scan_status = forms.IntegerField(required=False)


# 服务器发送脚本表单
class CreateServerAutoForm(forms.Form):
    ip_inner = forms.CharField(required=True, max_length=32)
    port = forms.IntegerField(required=True)
    os_status = forms.IntegerField(required=True)
    system_status = forms.IntegerField(required=True)