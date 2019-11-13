# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime

user_num = 3 #初始化用户数

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
    isname = User.objects.filter(username = 'admin')
    if isname:
        user = User.objects.get(username='admin')
        user.set_password('admin')
        user.save()
    else:
        User.objects.create_superuser('admin', 'admin@test.com','admin')
    
    #print('===='+os.getcwd()) #当前目录
    
    # 菜单 初始化 *个菜单
    menulist = ['HOME','采购管理','财务管理','客户管理','信息管理','角色管理','用户管理','菜单管理','权限管理']
    for i in menulist:
        m = Menu()
        m.title = i
        m.save()
    
    # 权限 初始化 *个权限   
    perlistdict = [['HOME',['test','/bank/test/test/','test_test']],\
                   ['HOME',['首页','/bank/index/','bank_index']],\
                   ['',['帮助文档','/bank/help/(.+)','help']],\
                    ['',['上传文件','/bank/upload/','upload_word_tpl']],\
                    ['',['下载文件','/bank/download/','download_word_tpl']],\
                   
                   ['采购管理',['采购列表','/web/purchase/list/(.+)','purchase_list']],\
                   ['',['添加采购','/web/purchase/add/','purchase_add']],\
                   ['',['删除采购','/web/purchase/del/(?P<cid>\d+)/$','purchase_del']],\
                   ['',['修改采购','/web/purchase/edit/(?P<cid>\d+)/$','purchase_edit']],\
                   ['',['批量采购导入','/web/purchase/import/','purchase_import']],\
                   ['',['下载采购模板','/web/purchase/tpl/','purchase_tpl']],\
                   
                   ['财务管理',['送货列表','/web/delivery/list/(.+)','delivery_list']],\
                   ['',['添加送货','/web/delivery/add/','delivery_add']],\
                   ['',['修改送货','/web/delivery/edit/(?P<cid>\d+)/$','delivery_edit']],\
                   ['',['删除送货','/web/delivery/del/(?P<cid>\d+)/$','delivery_del']],\
                   ['',['批量导入送货','/web/delivery/import/','delivery_import']],\
                   ['',['下载送货模板','/web/delivery/tpl/','delivery_tpl']],\
                   
                   ['',['下载送货单页电子表格','/web/makexlsx/page/(.+)','makexlsx_page']],\
                   ['',['下载送货全部电子表格','/web/makexlsx/all/(.+)','makexlsx_all']],\
                   
                   ['',['批量导入销售成本','/web/cost/import/','cost_import']],\
                   ['财务管理',['销售成本列表','/web/cost/list/(.+)','cost_list']],\
                   ['',['添加销售成本','/web/cost/add/','cost_add']],\
                   ['',['修改销售成本','/web/cost/edit/(?P<cid>\d+)/$','cost_edit']],\
                   ['',['删除销售成本','/web/cost/del/(?P<cid>\d+)/$','cost_del']],\
                   ['',['销售成本利润图形','/web/profit/graph/','profit_graph']],\
                   
                   ['',['下载销售成本单页电子表格','/web/cost/makexlsx/page/(.+)','cost_makexlsx_page']],\
                   ['',['下载销售成本全部电子表格','/web/cost/makexlsx/all/(.+)','cost_makexlsx_all']],\
                   
                                      
                   ['',['批量导入应付账款','/web/copewith/import/','copewith_import']],\
                   ['',['下载应付账款模板','/web/copewith/tpl/','copewith_tpl']],\
                   ['财务管理',['应付账款列表','/web/copewith/list/(.+)','copewith_list']],\
                   ['',['添加应付账款','/web/copewith/add/','copewith_add']],\
                   ['',['修改应付账款','/web/copewith/edit/(?P<cid>\d+)/$','copewith_edit']],\
                   ['',['删除应付账款','/web/copewith/del/(?P<cid>\d+)/$','copewith_del']],\
                   ['',['下载应付账款单页电子表格','/web/copewith/makexlsx/page/(.+)','copewith_makexlsx_page']],\
                   ['',['下载应付账款全部电子表格','/web/copewith/makexlsx/all/(.+)','copewith_makexlsx_all']],\
                   
                    ['',['批量导入应收账款','/web/receivable/import/','receivable_import']],\
                    ['',['下载应收账款模板','/web/receivable/tpl/','receivable_tpl']],\
                    ['财务管理',['应收账款列表','/web/receivable/list/(.+)','receivable_list']],\
                    ['',['添加应收账款','/web/receivable/add/','receivable_add']],\
                    ['',['修改应收账款','/web/receivable/edit/(?P<cid>\d+)/$','receivable_edit']],\
                    ['',['删除应收账款','/web/receivable/del/(?P<cid>\d+)/$','receivable_del']],\
                   ['',['下载应收账款单页电子表格','/web/receivable/makexlsx/page/(.+)','receivable_makexlsx_page']],\
                   ['',['下载应收账款全部电子表格','/web/receivable/makexlsx/all/(.+)','receivable_makexlsx_all']],\


                    ['',['批量导入材料报表','/web/materialreport/import/','materialreport_import']],\
                    ['',['下载材料报表模板','/web/materialreport/tpl/','materialreport_tpl']],\
                    ['财务管理',['材料报表列表','/web/materialreport/list/(.+)','materialreport_list']],\
                    ['',['添加材料报表','/web/materialreport/add/','materialreport_add']],\
                    ['',['修改材料报表','/web/materialreport/edit/(?P<cid>\d+)/$','materialreport_edit']],\
                    ['',['删除材料报表','/web/materialreport/del/(?P<cid>\d+)/$','materialreport_del']],\
                    ['',['下载材料报表单页电子表格','/web/materialreport/makexlsx/page/(.+)','materialreport_makexlsx_page']],\
                    ['',['下载材料报表全部电子表格','/web/materialreport/makexlsx/all/(.+)','materialreport_makexlsx_all']],\

                    ['',['批量导入产销存报表','/web/salesreport/import/','salesreport_import']],\
                    ['',['下载产销存报表模板','/web/salesreport/tpl/','salesreport_tpl']],\
                    ['财务管理',['产销存列表','/web/salesreport/list/(.+)','salesreport_list']],\
                    ['',['添加产销存报表','/web/salesreport/add/','salesreport_add']],\
                    ['',['修改产销存报表','/web/salesreport/edit/(?P<cid>\d+)/$','salesreport_edit']],\
                    ['',['删除产销存报表','/web/salesreport/del/(?P<cid>\d+)/$','salesreport_del']],\
                    ['',['下载产销存报表单页电子表格','/web/salesreport/makexlsx/page/(.+)','salesreport_makexlsx_page']],\
                    ['',['下载产销存报表全部电子表格','/web/salesreport/makexlsx/all/(.+)','salesreport_makexlsx_all']],\

                    ['',['批量导入领料汇总','/web/picking/import/','picking_import']],\
                    ['',['下载领料汇总模板','/web/picking/tpl/','picking_tpl']],\
                    ['财务管理',['领料汇总列表','/web/picking/list/(.+)','picking_list']],\
                    ['',['添加领料汇总','/web/picking/add/','picking_add']],\
                    ['',['修改领料汇总','/web/picking/edit/(?P<cid>\d+)/$','picking_edit']],\
                    ['',['删除领料汇总','/web/picking/del/(?P<cid>\d+)/$','picking_del']],\
                    ['',['下载领料汇总单页电子表格','/web/picking/makexlsx/page/(.+)','picking_makexlsx_page']],\
                    ['',['下载领料汇总全部电子表格','/web/picking/makexlsx/all/(.+)','picking_makexlsx_all']],\

                    ['',['批量导入成品入库','/web/warehousing/import/','warehousing_import']],\
                    ['',['下载成品入库模板','/web/warehousing/tpl/','warehousing_tpl']],\
                    ['财务管理',['成品入库列表','/web/warehousing/list/(.+)','warehousing_list']],\
                    ['',['添加成品入库','/web/warehousing/add/','warehousing_add']],\
                    ['',['修改成品入库','/web/warehousing/edit/(?P<cid>\d+)/$','warehousing_edit']],\
                    ['',['删除成品入库','/web/warehousing/del/(?P<cid>\d+)/$','warehousing_del']],\
                    ['',['下载成品入库单页电子表格','/web/warehousing/makexlsx/page/(.+)','warehousing_makexlsx_page']],\
                    ['',['下载成品入库全部电子表格','/web/warehousing/makexlsx/all/(.+)','warehousing_makexlsx_all']],\

                    ['',['批量导入材料入库','/web/materialstorage/import/','materialstorage_import']],\
                    ['',['下载材料入库模板','/web/materialstorage/tpl/','materialstorage_tpl']],\
                    ['财务管理',['材料入库列表','/web/materialstorage/list/(.+)','materialstorage_list']],\
                    ['',['添加材料入库','/web/materialstorage/add/','materialstorage_add']],\
                    ['',['修改材料入库','/web/materialstorage/edit/(?P<cid>\d+)/$','materialstorage_edit']],\
                    ['',['删除材料入库','/web/materialstorage/del/(?P<cid>\d+)/$','materialstorage_del']],\
                    ['',['下载材料入库单页电子表格','/web/materialstorage/makexlsx/page/(.+)','materialstorage_makexlsx_page']],\
                    ['',['下载材料入库全部电子表格','/web/materialstorage/makexlsx/all/(.+)','materialstorage_makexlsx_all']],\
                   
                                      
                   ['客户管理',['客户列表','/web/customer/list/','customer_list']],\
                   ['',['添加客户','/web/customer/add/','customer_add']],\
                   ['',['删除客户','/web/customer/del/(?P<cid>\d+)/$','customer_del']],\
                   ['',['修改客户','/web/customer/edit/(?P<cid>\d+)/$','customer_edit']],\
                   ['',['批量导入','/web/customer/import/','customer_import']],\
                   ['',['下载模板','/web/customer/tpl/','customer_tpl']],\
                                    
                   ['信息管理',['账单列表','/web/payment/list/','payment_list']],\
                   ['',['添加账单','/web/payment/add/','payment_add']],\
                   ['',['删除账单','/web/payment/del/(?P<cid>\d+)/$','payment_del']],\
                   ['',['修改账单','/web/payment/edit/(?P<cid>\d+)/$','payment_edit']],\
                   
                    ['角色管理',['角色列表','/rbac/role/list/','role_list']],\
                    ['角色管理',['添加角色','/rbac/role/add/','role_add']],\
                    ['',['删除角色','/rbac/role/del/(?P<cid>\d+)/$','role_del']],\
                    ['',['修改角色','/rbac/role/edit/(?P<cid>\d+)/$','role_edit']],\
                    
                    ['用户管理',['用户列表','/rbac/user/list/','user_list']],\
                    ['',['添加用户','/rbac/user/add/','user_add']],\
                    ['',['删除用户','/rbac/user/del/(?P<cid>\d+)/$','user_del']],\
                    ['',['修改用户','/rbac/user/edit/(?P<cid>\d+)/$','user_edit']],\
                    ['',['重置密码','/rbac/user/reset/password/(?P<cid>\d+)/$','user_reset_pwd']],\
                    ['',['批量用户导入','/rbac/user/import/','user_import']],\
                    ['',['下载用户模板','/rbac/user/tpl/','user_tpl']],\
                                        
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
                                        
                    
                   ]
    
    for d in perlistdict:
        p = Permission()
        p.title = d[1][0]
        p.url = d[1][1]
        p.name = d[1][2]
        if d[0]:
            p.menu =  Menu.objects.get(title = d[0])
        p.save()
                
    # 角色 初始化 -- 3个角色(CEO、主管、普通用户) 
    
    # CEO -- 具有所有权限 
    r = Role()
    r.title = 'CEO'
    r.save()    
    r = Role.objects.get(title = 'CEO') 
    r.permissions.add(Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '上传文件'),\
                      Permission.objects.get(title = '下载文件'),\
                      
                      Permission.objects.get(title = '采购列表'),\
                      Permission.objects.get(title = '添加采购'),\
                      Permission.objects.get(title = '删除采购'),\
                      Permission.objects.get(title = '修改采购'),\
                      Permission.objects.get(title = '批量采购导入'),\
                      Permission.objects.get(title = '下载采购模板'),\
                      
                      Permission.objects.get(title = '送货列表'),\
                      Permission.objects.get(title = '添加送货'),\
                      Permission.objects.get(title = '修改送货'),\
                      Permission.objects.get(title = '删除送货'),\
                      Permission.objects.get(title = '批量导入送货'),\
                      Permission.objects.get(title = '下载送货模板'),\
                      Permission.objects.get(title = '下载送货单页电子表格'),\
                      Permission.objects.get(title = '下载送货全部电子表格'),\
                      
                      Permission.objects.get(title = '批量导入销售成本'),\
                      Permission.objects.get(title = '销售成本列表'),\
                      Permission.objects.get(title = '添加销售成本'),\
                      Permission.objects.get(title = '修改销售成本'),\
                      Permission.objects.get(title = '删除销售成本'),\
                      Permission.objects.get(title = '销售成本利润图形'),\
                      Permission.objects.get(title = '下载销售成本单页电子表格'),\
                      Permission.objects.get(title = '下载销售成本全部电子表格'),\
                      
                      Permission.objects.get(title = '批量导入应付账款'),\
                      Permission.objects.get(title = '下载应付账款模板'),\
                      Permission.objects.get(title = '应付账款列表'),\
                      Permission.objects.get(title = '添加应付账款'),\
                      Permission.objects.get(title = '修改应付账款'),\
                      Permission.objects.get(title = '删除应付账款'),\
                      Permission.objects.get(title = '下载应付账款单页电子表格'),\
                      Permission.objects.get(title = '下载应付账款全部电子表格'),\
                                                                  
                    Permission.objects.get(title = '批量导入应收账款'),\
                    Permission.objects.get(title = '下载应收账款模板'),\
                    Permission.objects.get(title = '应收账款列表'),\
                    Permission.objects.get(title = '添加应收账款'),\
                    Permission.objects.get(title = '修改应收账款'),\
                    Permission.objects.get(title = '删除应收账款'),\
                    Permission.objects.get(title = '下载应收账款单页电子表格'),\
                    Permission.objects.get(title = '下载应收账款全部电子表格'),\
                      
                    Permission.objects.get(title = '批量导入材料报表'),\
                    Permission.objects.get(title = '下载材料报表模板'),\
                    Permission.objects.get(title = '材料报表列表'),\
                    Permission.objects.get(title = '添加材料报表'),\
                    Permission.objects.get(title = '修改材料报表'),\
                    Permission.objects.get(title = '删除材料报表'),\
                    Permission.objects.get(title = '下载材料报表单页电子表格'),\
                    Permission.objects.get(title = '下载材料报表全部电子表格'),\

                    Permission.objects.get(title = '批量导入产销存报表'),\
                    Permission.objects.get(title = '下载产销存报表模板'),\
                    Permission.objects.get(title = '产销存列表'),\
                    Permission.objects.get(title = '添加产销存报表'),\
                    Permission.objects.get(title = '修改产销存报表'),\
                    Permission.objects.get(title = '删除产销存报表'),\
                    Permission.objects.get(title = '下载产销存报表单页电子表格'),\
                    Permission.objects.get(title = '下载产销存报表全部电子表格'),\

                    Permission.objects.get(title = '批量导入领料汇总'),\
                    Permission.objects.get(title = '下载领料汇总模板'),\
                    Permission.objects.get(title = '领料汇总列表'),\
                    Permission.objects.get(title = '添加领料汇总'),\
                    Permission.objects.get(title = '修改领料汇总'),\
                    Permission.objects.get(title = '删除领料汇总'),\
                    Permission.objects.get(title = '下载领料汇总单页电子表格'),\
                    Permission.objects.get(title = '下载领料汇总全部电子表格'),\

                    Permission.objects.get(title = '批量导入材料入库'),\
                    Permission.objects.get(title = '下载材料入库模板'),\
                    Permission.objects.get(title = '材料入库列表'),\
                    Permission.objects.get(title = '添加材料入库'),\
                    Permission.objects.get(title = '修改材料入库'),\
                    Permission.objects.get(title = '删除材料入库'),\
                    Permission.objects.get(title = '下载材料入库单页电子表格'),\
                    Permission.objects.get(title = '下载材料入库全部电子表格'),\

                    Permission.objects.get(title = '批量导入成品入库'),\
                    Permission.objects.get(title = '下载成品入库模板'),\
                    Permission.objects.get(title = '成品入库列表'),\
                    Permission.objects.get(title = '添加成品入库'),\
                    Permission.objects.get(title = '修改成品入库'),\
                    Permission.objects.get(title = '删除成品入库'),\
                    Permission.objects.get(title = '下载成品入库单页电子表格'),\
                    Permission.objects.get(title = '下载成品入库全部电子表格'),\

                                            
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
                                     
                    )
    r.save()

    # 主管 -- 没有删除权限
    r = Role()
    r.title = '主管'
    r.save()    
    r = Role.objects.get(title = '主管')
    r.permissions.add(Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '上传文件'),\
                      Permission.objects.get(title = '下载文件'),\
                      
                      Permission.objects.get(title = '采购列表'),\
                      Permission.objects.get(title = '添加采购'),\
                      Permission.objects.get(title = '删除采购'),\
                      Permission.objects.get(title = '修改采购'),\
                      Permission.objects.get(title = '批量采购导入'),\
                      Permission.objects.get(title = '下载采购模板'),\
                      )
    r.save()

    # 普通用户 -- 只有首页、客户列表、账单列表3个权限
    r = Role()
    r.title = '普通用户'
    r.save()    
    r = Role.objects.get(title = '普通用户')
    r.permissions.add(Permission.objects.get(title = '首页'),\
                      Permission.objects.get(title = '帮助文档'),\
                      Permission.objects.get(title = '上传文件'),\
                      Permission.objects.get(title = '下载文件'),\
        
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
        
    #付费金额
    moneys = [100, 200, 300, 400]
    # 账单 初始化 -- 4个账单
    for n, i in enumerate(customers):
        p = Payment()
        p.customer = Customer.objects.get(name = i[0]) 
        p.money = moneys[n]
        p.save()  

     
        