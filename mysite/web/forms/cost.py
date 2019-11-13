#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class CostForm(ModelForm):
    class Meta:
        model = models.Cost
        fields = ["date","name","voucherno","abstract","invoice","delivery",\
         "cost_amount","meals","travel_expenses","gift",\
         "cash_gift","recreation","car","cost_rate",\
         "return_freight","special_car","customer_claims","payment_commission","other"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

