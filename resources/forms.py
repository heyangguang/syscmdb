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
