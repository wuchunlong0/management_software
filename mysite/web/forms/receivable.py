#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class ReceivableForm(ModelForm):
    class Meta:
        model = models.Receivable
        fields = ["date","name","receipt","abstract","number",\
                  "univalence","collection","note","date1",\
                  "Invoice_number","money1"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ReceivableForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

