#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect

from web import models
from web.forms.payment import PaymentForm, PaymentUserForm


def payment_list(request):
    """
    付费列表
    :return:
    """
    data_list = models.Payment.objects.all()
    return render(request, 'web/payment/payment_list.html', context=locals())

def payment_add(request):
    """
    编辑付费记录
    :return:
    """
    if request.method == 'GET':
        form = PaymentForm()
        return render(request, 'web/form_submit.html', context=locals())
    form = PaymentForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/web/payment/list/') 
    return render(request, 'web/form_submit.html', context=locals())


def payment_edit(request, pid):
    """
    编辑付费记录
    :return:
    """
    obj = models.Payment.objects.get(id=pid)
    if request.method == 'GET':
        form = PaymentForm(instance=obj)
        return render(request, 'web/form_submit.html', context=locals())
    form = PaymentForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/web/payment/list/')
    return render(request, 'web/form_submit.html', context=locals())


def payment_del(request, pid):
    """
    删除付费记录
    :param request:
    :param cid:
    :return:
    """
    models.Payment.objects.filter(id=pid).delete()
    return redirect('/web/payment/list/')
