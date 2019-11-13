#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class PickingForm(ModelForm):
    class Meta:
        model = models.Picking
        fields = ["date", "name","receipt","material_name","number",\
         "univalence","product_name","remarks"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PickingForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

