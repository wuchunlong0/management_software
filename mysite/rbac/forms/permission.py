#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from rbac import models


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'name',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),\
            'url': forms.TextInput(attrs={'class': 'form-control'}),\
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class UpdatePermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'name',]

    def __init__(self, *args, **kwargs):
        super(UpdatePermissionModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
