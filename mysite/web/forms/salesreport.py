#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class SalesreportForm(ModelForm):
    class Meta:
        model = models.Salesreport
        fields = ["date", "name","product_name","lastmonth_number", "lastmonth_univalence",\
        "thismonth_production_number","thismonth_production_univalence","thismonth_material","thismonth_artificial","thismonth_cost",\
        "return_number","return_money","purchase_number","purchase_money",\
        "collaruse_number","collaruse_money","weighting_number","weighting_univalence",\
        "goback_number","goback_money","nullify_number", "nullify_money","sample_sales_number",\
        "sample_sales_money","thismonth_number","thismonth_univalence"]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SalesreportForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

