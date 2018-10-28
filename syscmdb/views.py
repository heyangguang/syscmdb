# _*_ coding: utf-8 _*_
__author__ = 'HeYang'


from django.shortcuts import render


def page_not_found(request):
    return render(request, 'public/404.html')


def page_error(request):
    return render(request, 'public/500.html')