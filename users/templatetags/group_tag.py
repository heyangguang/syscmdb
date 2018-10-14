# _*_ coding: utf-8 _*_
__author__ = 'HeYang'
from django import template


# register固定写法，不可以变
register = template.Library()

@register.filter
def group_count(group_list):
    group_count = len(list(group_list))

    return group_count