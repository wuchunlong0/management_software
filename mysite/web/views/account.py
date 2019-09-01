#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rbac.service.init_permission import init_permission
from rbac import models
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'GET':
        error = request.GET.get('error')
        return render(request, 'login.html',context=locals())

    name = request.POST.get('username')
    pwd = request.POST.get('password')

    user_object = models.UserInfo.objects.filter(name=name, password=pwd).first()
    if not user_object:
        error = '用户名或密码错误!'
        return render(request, 'login.html', context=locals())

    
    if User.objects.filter(username = name):
        user = User.objects.get(username=name)
    else:
        user = User.objects.create_user(name, 'test@test.com',pwd)    
    auth_login(request, user)

    # 用户权限信息的初始化
    init_permission(user_object, request)
    return redirect('/bank/index/')
    return redirect('/customer/list/')
