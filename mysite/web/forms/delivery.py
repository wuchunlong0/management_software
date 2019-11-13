#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class DeliveryForm(ModelForm):
    class Meta:
        model = models.Delivery
        fields = ['date','name','num','customer','product','number','price','note']
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

