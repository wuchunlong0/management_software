#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models

class MaterialreportForm(ModelForm):
    class Meta:
        model = models.Materialreport
        fields = ["date","name","material_name","lastmonth_number","lastmonth_univalence",\
                  "income_number","income_univalence","weighting_number","weighting_univalence",\
                  "production_expenditure_number","production_expenditure_univalence",\
                  "material_expenditure_number","material_expenditure_money",\
                  "sale_number","sale_money","thismonth_number","thismonth_univalence",]
        #fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MaterialreportForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

