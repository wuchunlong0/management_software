# -*- coding: UTF-8 -*-
from django.contrib import admin
from .models import UserInfo, Role, Permission, Menu 
    
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):    
    list_display = ('id', 'title', 'icon', )


@admin.register(UserInfo)    
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'password', 'email', 'role_list')
    def role_list(self, userInfo):
        """自定义列表字段"""
        return [u.title for u in userInfo.roles.all()]
        #tag_permissions = map(lambda x: x.title, userInfo.roles.all())
        #return ', '.join(tag_permissions)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):   
    list_display = ('id', 'title', 'permissions_list')
    def permissions_list(self, role):
        """自定义列表字段"""
        return [u.title for u in role.permissions.all()]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):    
    list_display = ('id', 'title', 'url', 'name','menu','pid')

