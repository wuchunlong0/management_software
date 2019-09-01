# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Bankemploye, Bankuser, Contacts,Setvalue

@admin.register(Bankemploye)
class BankemployeAdmin(admin.ModelAdmin):    
    list_display = ('id','serialNumber','title','subitem','drivingfactors','investigation',\
        'classificationNumber','score','dimensionalItems','remarks',\
        'a_analyse', 'b_analyse', 'c_analyse', 'd_analyse', 'e_analyse',\
        'a','b','c','d','e',\
        'a_per','b_per','c_per','d_per','e_per')

@admin.register(Bankuser)
class BankuserAdmin(admin.ModelAdmin):    
    list_display = ('id', 'name', 'title','ask', 'reply')
    
@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):    
    list_display = ('id','name','email','tel','content','date')

@admin.register(Setvalue)
class SetvalueAdmin(admin.ModelAdmin):    
    list_display = ('id','a_per','b_per','c_per','d_per','e_per')
