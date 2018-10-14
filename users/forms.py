# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django import forms
from django.contrib.auth.models import Group, ContentType


# 创建用户表单
class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=4, required=True)
    email = forms.EmailField(required=True)
    is_superuser = forms.IntegerField(required=True)


class CreateProfileForm(forms.Form):
    name = forms.CharField(required=True, max_length=10)
    lnvalid_date = forms.CharField(required=True, max_length=35)
    phone = forms.CharField(required=True, min_length=11)
    weixin = forms.CharField(required=True)


class CreatePermForm(forms.Form):
    name = forms.CharField(required=True)
    content_type = forms.IntegerField(required=True)
    codename = forms.CharField(required=True)

    def clean_content_type(self):
        context_type_id = self.cleaned_data['content_type']

        try:
            return ContentType.objects.get(pk=context_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError('此模型不存在')