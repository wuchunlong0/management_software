from django.conf.urls import url
from web.views import customer
from web.views import payment
from web.views import purchase
from web.views import delivery
from web.views import cost
from web.views import copewith
from web.views import receivable
from web.views import materialreport,salesreport,picking,warehousing,materialstorage

#
urlpatterns = [
    url(r'^customer/list/$', customer.customer_list, name='customer_list'),
    url(r'^customer/add/$', customer.customer_add, name='customer_add'),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name='customer_edit'),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name='customer_del'),
    url(r'^customer/import/$', customer.customer_import, name='customer_import'),
    url(r'^customer/tpl/$', customer.customer_tpl, name='customer_tpl'),

    url(r'^payment/list/$', payment.payment_list, name='payment_list'),
    url(r'^payment/add/$', payment.payment_add, name='payment_add'),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit, name='payment_edit'),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del, name='payment_del'),

    # 采购模块
    url(r'^purchase/list/(.+)', purchase.purchase_list, name='purchase_list'),
    url(r'^purchase/add/$', purchase.purchase_add, name='purchase_add'),
    url(r'^purchase/edit/(?P<cid>\d+)/$', purchase.purchase_edit, name='purchase_edit'),
    url(r'^purchase/del/(?P<cid>\d+)/$', purchase.purchase_del, name='purchase_del'),    
    url(r'^purchase/import/$', purchase.purchase_import, name='purchase_import'),
    url(r'^purchase/tpl/$', purchase.purchase_tpl, name='purchase_tpl'),

    # 送货模块
    url(r'^delivery/list/(.+)', delivery.delivery_list, name='delivery_list'),
    url(r'^delivery/add/$', delivery.delivery_add, name='delivery_add'),
    url(r'^delivery/edit/(?P<cid>\d+)/$', delivery.delivery_edit, name='delivery_edit'),
    url(r'^delivery/del/(?P<cid>\d+)/$', delivery.delivery_del, name='delivery_del'),
    url(r'^delivery/import/$', delivery.delivery_import, name='delivery_import'),
    url(r'^delivery/tpl/$', delivery.delivery_tpl, name='delivery_tpl'),    
    url(r'^makexlsx/page/(.+)', delivery.makexlsx_page, name='makexlsx_page'),
    url(r'^makexlsx/all/(.+)', delivery.makexlsx_all, name='makexlsx_all'),

    #销售成本  
    url(r'^cost/import/$', cost.cost_import, name='cost_import'),
    url(r'^cost/list/(.+)', cost.cost_list, name='cost_list'),
    url(r'^cost/add/', cost.cost_add, name='cost_add'),
    url(r'^cost/edit/(?P<cid>\d+)/$', cost.cost_edit, name='cost_edit'),
    url(r'^cost/del/(?P<cid>\d+)/$', cost.cost_del, name='cost_del'),
    url(r'^profit/graph/', cost.profit_graph, name='profit_graph'),  #销售成本利润图形    
    url(r'^cost/makexlsx/page/(.+)', cost.cost_makexlsx_page, name='cost_makexlsx_page'),
    url(r'^cost/makexlsx/all/(.+)', cost.cost_makexlsx_all, name='cost_makexlsx_all'),
        
    #应付账款
    url(r'^copewith/import/$', copewith.copewith_import, name='copewith_import'),
    url(r'^copewith/tpl/', copewith.copewith_tpl, name='copewith_tpl'),
    url(r'^copewith/list/(.+)', copewith.copewith_list, name='copewith_list'),
    url(r'^copewith/add/', copewith.copewith_add, name='copewith_add'),
    url(r'^copewith/edit/(?P<cid>\d+)/$', copewith.copewith_edit, name='copewith_edit'),
    url(r'^copewith/del/(?P<cid>\d+)/$', copewith.copewith_del, name='copewith_del'),
    url(r'^copewith/makexlsx/page/(.+)', copewith.copewith_makexlsx_page, name='copewith_makexlsx_page'),
    url(r'^copewith/makexlsx/all/(.+)', copewith.copewith_makexlsx_all, name='copewith_makexlsx_all'),

    #应收账款
    url(r'^receivable/import/$', receivable.receivable_import, name='receivable_import'),
    url(r'^receivable/tpl/', receivable.receivable_tpl, name='receivable_tpl'),
    url(r'^receivable/list/(.+)', receivable.receivable_list, name='receivable_list'),
    url(r'^receivable/add/', receivable.receivable_add, name='receivable_add'),
    url(r'^receivable/edit/(?P<cid>\d+)/$', receivable.receivable_edit, name='receivable_edit'),
    url(r'^receivable/del/(?P<cid>\d+)/$', receivable.receivable_del, name='receivable_del'),
    url(r'^receivable/makexlsx/page/(.+)', receivable.receivable_makexlsx_page, name='receivable_makexlsx_page'),
    url(r'^receivable/makexlsx/all/(.+)', receivable.receivable_makexlsx_all, name='receivable_makexlsx_all'),

    #材料报表
    url(r'^materialreport/import/$', materialreport.materialreport_import, name='materialreport_import'),
    url(r'^materialreport/tpl/', materialreport.materialreport_tpl, name='materialreport_tpl'),
    url(r'^materialreport/list/(.+)', materialreport.materialreport_list, name='materialreport_list'),
    url(r'^materialreport/add/', materialreport.materialreport_add, name='materialreport_add'),
    url(r'^materialreport/edit/(?P<cid>\d+)/$', materialreport.materialreport_edit, name='materialreport_edit'),
    url(r'^materialreport/del/(?P<cid>\d+)/$', materialreport.materialreport_del, name='materialreport_del'),
    url(r'^materialreport/makexlsx/page/(.+)', materialreport.materialreport_makexlsx_page, name='materialreport_makexlsx_page'),
    url(r'^materialreport/makexlsx/all/(.+)', materialreport.materialreport_makexlsx_all, name='materialreport_makexlsx_all'),

    #产销存报表
    url(r'^salesreport/import/$', salesreport.salesreport_import, name='salesreport_import'),
    url(r'^salesreport/tpl/', salesreport.salesreport_tpl, name='salesreport_tpl'),
    url(r'^salesreport/list/(.+)', salesreport.salesreport_list, name='salesreport_list'),
    url(r'^salesreport/add/', salesreport.salesreport_add, name='salesreport_add'),
    url(r'^salesreport/edit/(?P<cid>\d+)/$', salesreport.salesreport_edit, name='salesreport_edit'),
    url(r'^salesreport/del/(?P<cid>\d+)/$', salesreport.salesreport_del, name='salesreport_del'),
    url(r'^salesreport/makexlsx/page/(.+)', salesreport.salesreport_makexlsx_page, name='salesreport_makexlsx_page'),
    url(r'^salesreport/makexlsx/all/(.+)', salesreport.salesreport_makexlsx_all, name='salesreport_makexlsx_all'),

    #领料汇总
    url(r'^picking/import/$', picking.picking_import, name='picking_import'),
    url(r'^picking/tpl/', picking.picking_tpl, name='picking_tpl'),
    url(r'^picking/list/(.+)', picking.picking_list, name='picking_list'),
    url(r'^picking/add/', picking.picking_add, name='picking_add'),
    url(r'^picking/edit/(?P<cid>\d+)/$', picking.picking_edit, name='picking_edit'),
    url(r'^picking/del/(?P<cid>\d+)/$', picking.picking_del, name='picking_del'),
    url(r'^picking/makexlsx/page/(.+)', picking.picking_makexlsx_page, name='picking_makexlsx_page'),
    url(r'^picking/makexlsx/all/(.+)', picking.picking_makexlsx_all, name='picking_makexlsx_all'),

    #成品入库
    url(r'^warehousing/import/$', warehousing.warehousing_import, name='warehousing_import'),
    url(r'^warehousing/tpl/', warehousing.warehousing_tpl, name='warehousing_tpl'),
    url(r'^warehousing/list/(.+)', warehousing.warehousing_list, name='warehousing_list'),
    url(r'^warehousing/add/', warehousing.warehousing_add, name='warehousing_add'),
    url(r'^warehousing/edit/(?P<cid>\d+)/$', warehousing.warehousing_edit, name='warehousing_edit'),
    url(r'^warehousing/del/(?P<cid>\d+)/$', warehousing.warehousing_del, name='warehousing_del'),
    url(r'^warehousing/makexlsx/page/(.+)', warehousing.warehousing_makexlsx_page, name='warehousing_makexlsx_page'),
    url(r'^warehousing/makexlsx/all/(.+)', warehousing.warehousing_makexlsx_all, name='warehousing_makexlsx_all'),

    #材料入库
    url(r'^materialstorage/import/$', materialstorage.materialstorage_import, name='materialstorage_import'),
    url(r'^materialstorage/tpl/', materialstorage.materialstorage_tpl, name='materialstorage_tpl'),
    url(r'^materialstorage/list/(.+)', materialstorage.materialstorage_list, name='materialstorage_list'),
    url(r'^materialstorage/add/', materialstorage.materialstorage_add, name='materialstorage_add'),
    url(r'^materialstorage/edit/(?P<cid>\d+)/$', materialstorage.materialstorage_edit, name='materialstorage_edit'),
    url(r'^materialstorage/del/(?P<cid>\d+)/$', materialstorage.materialstorage_del, name='materialstorage_del'),
    url(r'^materialstorage/makexlsx/page/(.+)', materialstorage.materialstorage_makexlsx_page, name='materialstorage_makexlsx_page'),
    url(r'^materialstorage/makexlsx/all/(.+)', materialstorage.materialstorage_makexlsx_all, name='materialstorage_makexlsx_all'),
    
]
