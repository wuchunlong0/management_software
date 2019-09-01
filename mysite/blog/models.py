# -*- coding: utf-8 -*-
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    def __str__(self):
        return self.name
class Role(models.Model):
    title =models.CharField(max_length=32)
    #permissions = models.ManyToManyField(to="Permission")
    permissions = models.ForeignKey(Permission, on_delete=models.PROTECT)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32,default='1234qazx')
    email = models.EmailField()
    #roles = models.ManyToManyField(to="Role")
    roles = models.ForeignKey(Role, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
