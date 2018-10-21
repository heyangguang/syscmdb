# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django import template

# register固定写法，不可以变
register = template.Library()

@register.filter
def serveruser_count(server_list):
    return len(list(server_list))