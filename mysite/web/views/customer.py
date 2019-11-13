# -*- coding: utf-8 -*-
# 客户模块
import os
from django.shortcuts import render, redirect
from myAPI.downfileAPI import down_file
from django.conf import settings
import xlrd
from myAPI.excelAPI import post_excel_model_names
from web import models
from web.forms.customer import CustomerForm
from django.urls import reverse

def customer_list(request):
    """客户列表"""
    data_list = models.Customer.objects.all()
    return render(request, 'web/customer/customer_list.html', context=locals())

def customer_add(request):
    """编辑客户"""
    if request.method == 'GET':
        form = CustomerForm()
        return render(request, 'web/form_submit.html', context=locals())
    form = CustomerForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/web/customer/list/')
    return render(request, 'web/form_submit.html', context=locals())

def customer_edit(request, cid):
    """新增客户"""
    obj = models.Customer.objects.get(id=cid)
    if request.method == 'GET':
        form = CustomerForm(instance=obj)
        return render(request, 'web/form_submit.html', context=locals())
    form = CustomerForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/web/customer/list/')
    return render(request, 'web/form_submit.html', context=locals())

def customer_del(request, cid):
    """删除客户"""
    cancel = reverse('customer_list') #/customer/list/
    if request.method == 'GET':
        return render(request, 'web/del.html', context=locals())

    models.Customer.objects.filter(id=cid).delete()
    return redirect(cancel)


def customer_import(request):
    """批量导入 客户"""
    if request.method == 'GET':
        return render(request, 'web/customer/customer_import.html')
    
    k = ['name', 'age', 'email', 'company']
#     ret = post_excel_model_names(request, 'customer_excel', models.Customer, k)
#     if ret[0:3] == 'err':
#         context = {'status': False, 'msg': '导入失败. %s' %ret} 
#     else:    
    context = {'status': True, 'msg': '导入成功'} \
    if post_excel_model_names(request, 'customer_excel', models.Customer, k) \
    else {'status': False, 'msg': '导入失败'}    
    return render(request, 'web/customer/customer_import.html', context)

def customer_tpl(request):
    """下载客户模板"""
    tpl_path = os.path.join(settings.BASE_DIR, 'web', 'files', '批量导入客户模板.xlsx')
    return down_file(tpl_path, 'customer_excel_tpl.xlsx')
