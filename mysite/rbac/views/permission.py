#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
权限管理
wu-chun-long@outlook.com
CreateDate：2019.07.23
"""

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.permission import PermissionModelForm, UpdatePermissionModelForm

def permission_list(request):
    """权限列表"""
    permissions = models.Permission.objects.all()
    return render(request, 'rbac/permission_list.html', context=locals())

def permission_add(request):
    """添加权限"""
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/permission_add.html', context=locals())

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:permission_list'))
    return render(request, 'rbac/permission_add.html', context=locals())


def permission_edit(request, pk):
    """编辑权限"""
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('权限不存在')
    if request.method == 'GET':
        form = UpdatePermissionModelForm(instance=obj)
        return render(request, 'rbac/permission_add.html', context=locals())

    form = UpdatePermissionModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:permission_list'))
    return render(request, 'rbac/permission_add.html', context=locals())

def permission_del(request, pk):
    """删除权限"""
    cancel = reverse('rbac:permission_list')
    if request.method == 'GET':
        return render(request, 'rbac/permission_del.html', context=locals())

    models.Permission.objects.filter(id=pk).delete()
    return redirect(cancel)


