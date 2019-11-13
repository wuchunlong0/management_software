#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models


class PurchaseForm(ModelForm):
    class Meta:
        model = models.Purchase
        fields = ['name', 'product', 'number', 'price',  'payment', 'payment_method', 'note']
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

