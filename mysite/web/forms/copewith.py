#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class CopewithForm(ModelForm):
    class Meta:
        model = models.Copewith
        fields = ["date","name","receipt","abstract","payment","number",\
            "univalence","note","date1","Invoice_number","money1"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CopewithForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

