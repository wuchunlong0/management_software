# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='blog_index'),
    url(r'^user_list/', views.user_list, name='blog_user_list'), 
    url(r'^user_add/', views.user_add, name='blog_user_add'),     
    url(r'^user_edit/', views.user_edit, name='blog_user_edit'),
    url(r'^user_del/', views.user_del, name='blog_user_del'),  
       
]
