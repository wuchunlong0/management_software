# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Bankemploye(models.Model):
    serialNumber = models.CharField(max_length=4, null=True, blank=True) #序号
    title = models.CharField(max_length=128, null=True, blank=True) #调查总标题 满意度、敬业度、忠诚度    
    subitem = models.CharField(max_length=100, null=True, blank=True)  #分类子项
    drivingfactors = models.CharField(max_length=100, null=True, blank=True) #驱动因素项
    investigation = models.CharField(max_length=100, null=True, blank=True)  #调查题目
    classificationNumber = models.CharField(max_length=4, null=True, blank=True)  #分类项号
    score = models.CharField(max_length=4, null=True, blank=True)  #评分
    dimensionalItems = models.CharField(max_length=32, null=True, blank=True)  #分维度项
    remarks = models.CharField(max_length=32, null=True, blank=True)  #备注
    a_analyse = models.CharField(max_length=500, null=True, blank=True)  #分析原因、改进措施
    b_analyse = models.CharField(max_length=500, null=True, blank=True)  #分析
    c_analyse = models.CharField(max_length=500, null=True, blank=True)  #分析
    d_analyse = models.CharField(max_length=500, null=True, blank=True)  #分析
    e_analyse = models.CharField(max_length=500, null=True, blank=True)  #分析    
    a = models.IntegerField(default=0)
    b = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    d = models.IntegerField(default=0)
    e = models.IntegerField(default=0)
    a_per = models.FloatField(default=0)
    b_per = models.FloatField(default=0)
    c_per = models.FloatField(default=0)
    d_per = models.FloatField(default=0)
    e_per = models.FloatField(default=0)
    def __str__(self):
        return self.serialNumber


class Bankuser(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)   
    title = models.CharField(max_length=128, null=True, blank=True) #标题
    ask = models.CharField(max_length=100, null=True, blank=True)   #调查问题项  
    reply = models.IntegerField(default=0)
    def __str__(self):
        return self.name

#联系我们
class Contacts(models.Model):
    name = models.CharField(max_length=12,blank=True, null=True) #留言人
    email = models.CharField(max_length=24,blank=True, null=True)
    tel = models.CharField(max_length=16,blank=True, null=True)
    content = models.TextField(max_length=256,blank=True, null=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True) #自动创建日期含时间
    def __str__(self):
        return self.name
    
class Setvalue(models.Model):
    myid = models.IntegerField(default=0)
    a_per = models.FloatField(default=20)
    b_per = models.FloatField(default=20)
    c_per = models.FloatField(default=20)
    d_per = models.FloatField(default=20)
    e_per = models.FloatField(default=20)
    def __str__(self):
        return self.a_per
