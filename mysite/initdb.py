# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime

user_num = 1 #初始化用户数

# 登录用户 初始化
roots = []
for i in range(1,user_num+1): 
    if i == 1:
        roots.append(['root','123','user1@1.com','CEO'])
    elif i == 2:
        roots.append(['root2','123','user2@1.com','主管'])
    else:
        roots.append(['root%s' %i,'123','user@1.com','普通用户'])


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    from django.contrib.auth.models import User, Group, Permission
    from rbac.models import UserInfo, Role, Permission, Menu 
    from web.models import Customer, Payment    
    from bank.models import  Setvalue
    
    isname = User.objects.filter(username = 'admin')
    if isname:
        user = User.objects.get(username='admin')
        user.set_password('admin')
        user.save()
    else:
        User.objects.create_superuser('admin', 'admin@test.com','admin')
    
    #print('===='+os.getcwd()) #当前目录
    if os.path.exists("mysite/web/files/AnalysisReport.docx"):
        os.remove("mysite/web/files/AnalysisReport.docx") #删除分析报告文件
        print("del mysite/web/files/AnalysisReport.docx") 
    
    # 菜单 初始化 *个菜单
    menulist = ['HOME','问卷管理','客户管理','信息管理','角色管理','用户管理','菜单管理','权限管理','单元测试']
    for i in menulist:
        m = Menu()
        m.title = i
        m.save()
    
    # 权限 初始化 *个权限  
    perlistdict = [['HOME',['test','/bank/test/test/','test_test']],\
                   ['HOME',['首页','/bank/index/','bank_index']],\
                   ['',['帮助文档','/bank/help/(.+)','help']],\
                   ['',['联系我们','/bank/contactus/','contactus']],\
                   ['问卷管理',['上传问卷Excel','/bank/questionnaire/import/','questionnaire_import']],\
                   ['问卷管理',['问卷调查题库','/bank/inquire/into/','inquire_into']],\
                   ['问卷管理',['问卷查询','/bank/user/questionnaire/(.+)','user_questionnaire']],\
                   ['问卷管理',['数据统计保存为Excel','/bank/create/excel/','create_excel']],\
                   ['问卷管理',['总体评价','/bank/overall/evaluation/','overall_evaluation']],\
                   ['问卷管理',['问卷图表显示','/bank/all/investigation/','all_investigation']],\
                   ['问卷管理',['问卷图表显示排名','/bank/all/investigationRanking/','all_investigationRanking']],\
                   ['问卷管理',['设置阀值','/bank/setting/value/','setting_value/']],\
                   ['问卷管理',['显示阀值','/bank/setting/list/','setting_list/']],\
                   ['',['生成分析报告文件','/bank/analysis/report/','analysis_report']],\
                   ['问卷管理',['下载问卷模板','/bank/questionnaire/tpl/','questionnaire_tpl']],\
                   ['',['下载分析报告','/bank/down/analysisReport/','down_analysis_report']],\
                   ['',['上传文件','/bank/upload/','upload_word_tpl']],\
                   ['',['下载文件','/bank/download/','download_word_tpl']],\
                   
                   ['客户管理',['客户列表','/customer/list/','customer_list']],\
                   ['客户管理',['添加客户','/customer/add/','customer_add']],\
                   ['',['删除客户','/customer/del/(?P<cid>\d+)/$','customer_del']],\
                   ['',['修改客户','/customer/edit/(?P<cid>\d+)/$','customer_edit']],\
                   ['客户管理',['批量导入','/customer/import/','customer_import']],\
                   ['客户管理',['下载模板','/customer/tpl/','customer_tpl']],\
                   
                   
                   
                   ['信息管理',['账单列表','/payment/list/','payment_list']],\
                   ['信息管理',['添加账单','/payment/add/','payment_add']],\
                   ['',['删除账单','/payment/del/(?P<cid>\d+)/$','payment_del']],\
                   ['',['修改账单','/payment/edit/(?P<cid>\d+)/$','payment_edit']],\
                   
                    ['角色管理',['角色列表','/rbac/role/list/','role_list']],\
                    ['角色管理',['添加角色','/rbac/role/add/','role_add']],\
                    ['',['删除角色','/rbac/role/del/(?P<cid>\d+)/$','role_del']],\
                    ['',['修改角色','/rbac/role/edit/(?P<cid>\d+)/$','role_edit']],\
                    
                    ['用户管理',['用户列表','/rbac/user/list/','user_list']],\
                    ['用户管理',['添加用户','/rbac/user/add/','user_add']],\
                    ['',['删除用户','/rbac/user/del/(?P<cid>\d+)/$','user_del']],\
                    ['',['修改用户','/rbac/user/edit/(?P<cid>\d+)/$','user_edit']],\
                    ['',['重置密码','/rbac/user/reset/password/(?P<cid>\d+)/$','user_reset_pwd']],\
                    ['用户管理',['批量用户导入','/rbac/user/import/','user_import']],\
                    ['用户管理',['下载用户模板','/rbac/user/tpl/','user_tpl']],\
                                        
                    ['菜单管理',['菜单列表','/rbac/menu/list/','menu_list']],\
                    ['菜单管理',['添加菜单','/rbac/menu/add/','menu_add']],\
                    ['',['删除菜单','/rbac/menu/del/(?P<cid>\d+)/$','menu_del']],\
                    ['',['修改菜单','/rbac/menu/edit/(?P<cid>\d+)/$','menu_edit']],\
                    ['',['添加二级菜单','/rbac/second/menu/add/(?P<menu_id>\d+)/','second_menu_add']],\
                    ['',['删除二级菜单','/rbac/second/menu/del/(?P<pk>\d+)/$','second_menu_del']],\
                    ['',['修改二级菜单','/rbac/second/menu/edit/(?P<pk>\d+)/$','second_menu_edit']],\
                    
                    ['权限管理',['权限列表', '/rbac/permission/list/','permission_list']],\
                    ['权限管理',['增加权限', '/rbac/permission/add/','permission_add']],\
                    ['',['更改权限', '/rbac/permission/edit/(?P<pk>\d+)/$','permission_edit']],\
                    ['',['删去权限', '/rbac/permission/del/(?P<pk>\d+)/$','permission_del']],\
                    
                    ['权限管理',['分配权限','/rbac/distribute/permissions/','distribute_permissions']],\
                    ['权限管理',['批量操作权限','/rbac/multi/permissions/','multi_permissions']],\
                    ['',['添加权限','/rbac/menu/permission/add/(?P<second_menu_id>\d+)/$','menu_permission_add']],\
                    ['',['删除权限','/rbac/menu/permission/del/(?P<pk>\d+)/$','menu_permission_del']],\
                    ['',['修改权限','/rbac/menu/permission/edit/(?P<pk>\d+)/$','menu_permission_edit']],\
                    ['',['批量删除权限','/rbac/multi/permissions/del/(?P<pk>\d+)/$','multi_permissions_del']],\
                    
                    
                    ['单元测试',['问卷答题初始化','/bank/test/questionnaire/','test_questionnaire']],\
                    
                    
                   ]
    
    for d in perlistdict:
        p = Permission()
        p.title = d[1][0]
        p.url = d[1][1]
        p.name = d[1][2]
        if d[0]:
            p.menu =  Menu.objects.get(title = d[0])
        p.save()
                
    # 角色 初始化 -- 3个角色(CEO、主管、普通用户) contactus
    
    # CEO -- 具有所有权限 
    r = Role()
    r.title = 'CEO'
    r.save()    
    r = Role.objects.get(title = 'CEO') 
    r.permissions.add(Permission.objects.get(title = 'test'),\
                      Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '联系我们'),\
                      Permission.objects.get(title = '上传问卷Excel'),\
                      Permission.objects.get(title = '问卷调查题库'),\
                      Permission.objects.get(title = '问卷查询'),\
                      Permission.objects.get(title = '数据统计保存为Excel'),\
                      Permission.objects.get(title = '总体评价'),\
                      Permission.objects.get(title = '问卷图表显示'),\
                      Permission.objects.get(title = '问卷图表显示排名'),\
                      Permission.objects.get(title = '设置阀值'),\
                      Permission.objects.get(title = '显示阀值'),\
                      Permission.objects.get(title = '生成分析报告文件'),\
                      Permission.objects.get(title = '下载问卷模板'),\
                      Permission.objects.get(title = '下载分析报告'),\
                      Permission.objects.get(title = '上传文件'),\
                      Permission.objects.get(title = '上传文件'),\
                      
                      Permission.objects.get(title = '客户列表'),\
                      Permission.objects.get(title = '添加客户'),\
                      Permission.objects.get(title = '删除客户'),\
                      Permission.objects.get(title = '修改客户'),\
                      Permission.objects.get(title = '批量导入'),\
                      Permission.objects.get(title = '下载模板'),\
                      Permission.objects.get(title = '账单列表'),\
                      Permission.objects.get(title = '添加账单'),\
                      Permission.objects.get(title = '删除账单'),\
                      Permission.objects.get(title = '修改账单'),\
                    Permission.objects.get(title = '角色列表'),\
                    Permission.objects.get(title = '添加角色'),\
                    Permission.objects.get(title = '删除角色'),\
                    Permission.objects.get(title = '修改角色'),\
                    
                    Permission.objects.get(title = '用户列表'),\
                    Permission.objects.get(title = '添加用户'),\
                    Permission.objects.get(title = '删除用户'),\
                    Permission.objects.get(title = '修改用户'),\
                    Permission.objects.get(title = '重置密码'),\
                    Permission.objects.get(title = '批量用户导入'),\
                    Permission.objects.get(title = '下载用户模板'),\

                    Permission.objects.get(title = '菜单列表'),\
                    Permission.objects.get(title = '添加菜单'),\
                    Permission.objects.get(title = '删除菜单'),\
                    Permission.objects.get(title = '修改菜单'),\

                    Permission.objects.get(title = '添加二级菜单'),\
                    Permission.objects.get(title = '删除二级菜单'),\
                    Permission.objects.get(title = '修改二级菜单'),\

                    Permission.objects.get(title = '权限列表'),\
                    Permission.objects.get(title = '增加权限'),\
                    Permission.objects.get(title = '更改权限'),\
                    Permission.objects.get(title = '删去权限'),\
                    
                    Permission.objects.get(title = '添加权限'),\
                    Permission.objects.get(title = '删除权限'),\
                    Permission.objects.get(title = '修改权限'),\
                    
                    Permission.objects.get(title = '批量操作权限'),\
                    Permission.objects.get(title = '批量删除权限'),\
                    Permission.objects.get(title = '分配权限'),\
                    
                    Permission.objects.get(title = '问卷答题初始化'),\
                    
                    )
    r.save()

    # 主管 -- 没有删除权限
    r = Role()
    r.title = '主管'
    r.save()    
    r = Role.objects.get(title = '主管')
    r.permissions.add(Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '联系我们'),\
                      Permission.objects.get(title = '问卷调查题库'),\
                      Permission.objects.get(title = '客户列表'),\
                      Permission.objects.get(title = '添加客户'),\
                      Permission.objects.get(title = '修改客户'),\
                      Permission.objects.get(title = '批量导入'),\
                      Permission.objects.get(title = '下载模板'),\
                      Permission.objects.get(title = '账单列表'),\
                      Permission.objects.get(title = '添加账单'),\
                      Permission.objects.get(title = '修改账单'),\
                      )
    r.save()

    # 普通用户 -- 只有首页、客户列表、账单列表3个权限
    r = Role()
    r.title = '普通用户'
    r.save()    
    r = Role.objects.get(title = '普通用户')
    r.permissions.add(Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '联系我们'),\
                      Permission.objects.get(title = '问卷调查题库'),\
                      )
    r.save()
    
    #添加用户 
    for i in roots:
        u = UserInfo()
        u.name = i[0]
        u.password = i[1]
        u.email = i[2]
        u.save()    
    #添加用户角色 
    for i in roots:
        u = UserInfo.objects.get(name = i[0])
        u.roles.add(Role.objects.get(title = i[3]))   
        u.save()
        
    # 客户 初始化 -- 4个客户
    customers = [['王磊',28,'user1@1.com','中国石油公司'],\
                 ['李伟中',12,'user2@1.com','中国烟草公司'],\
                 ['赵云',22,'user3@1.com','中国人民银行'],\
                 ['张国力',36,'user4@1.com','中国成品油公司']]
    for i in customers:
        c = Customer()
        c.name = i[0]
        c.age = i[1]
        c.email = i[2]
        c.company = i[3]
        c.save()
        
    # 账单 初始化 -- 4个账单
    for i in customers:
        p = Payment()
        p.customer = Customer.objects.get(name = i[0]) 
        p.money = random.randint(1, 5) #1-5随机整数
        p.save()  

    s = Setvalue()
    s.a_per = 20
    s.b_per = 20
    s.c_per = 20
    s.d_per = 20
    s.e_per = 20
    s.save()

'''    
    # 初始化问卷 3人 
    from bank.models import Bankemploye, Bankuser
    investigation_list = Bankemploye.objects.values_list('investigation', flat=True).order_by('id')
    for r in roots:
        for i in investigation_list:
            b = Bankuser()
            b.name = r[0]
            b.ask = i
            b.reply = str(random.randint(1, 5))
            b.save()
'''   
    
    
    
        