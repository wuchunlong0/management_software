#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class WarehousingForm(ModelForm):
    class Meta:
        model = models.Warehousing
        fields = ["date", "name","receipt","product_name","number",\
         "univalence","remarks"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WarehousingForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

