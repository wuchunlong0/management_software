#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
用户管理
"""
import os
import xlrd
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPasswordUserModelForm
from myAPI.downfileAPI import down_file
from myAPI.excelAPI import post_excel_model, post_excel_model_name
from django.forms.models import model_to_dict

def user_list(request):
    """用户列表"""
    user_all = models.UserInfo.objects.all()
    users = []
    for user in user_all:
        if user.roles.all():
            users.append(dict(model_to_dict(user),**{'role' : user.roles.all()[0].title}))
        else:
            users.append(dict(model_to_dict(user),**{'role' : ''}))
            
    return render(request, 'rbac/user_list.html', context=locals())

def user_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/user_add.html', context=locals())

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        name = request.POST.get('name','')
        if models.UserInfo.objects.filter(name=name):
            meg = '%s 用户已经注册' % name
            return render(request, 'rbac/user_add.html', context=locals())
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_add.html', context=locals())

def user_edit(request, pk):
    """编辑用户"""
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        return render(request, 'rbac/user_add.html', context=locals())

    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_add.html', context=locals())

def user_reset_pwd(request, pk):
    """重置密码"""
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/user_add.html', context=locals())

    form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_add.html', context=locals())

def user_del(request, pk):
    """删除用户"""
    cancel = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/user_del.html', context=locals())

    models.UserInfo.objects.filter(id=pk).delete()
    return redirect(cancel)


def user_import(request):
    """用户批量导入"""
    if request.method == 'GET':
        return render(request, 'rbac/user_import.html')     
    k = ['name', 'password', 'email']    
    if post_excel_model_name(request, 'user_excel', models.UserInfo, k):
        return redirect(reverse('rbac:user_list'))    
    context = {'status': False, 'msg': '导入失败'}    
    return render(request, 'rbac/user_import.html', context)

def user_tpl(request):
    """下载用户模板"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入用户模板.xlsx')
    return down_file(tpl_path, 'user_excel_tpl.xlsx')
