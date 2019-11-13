# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone as timezone

class Cname(models.Model): 
    name = models.CharField(verbose_name='供货商名称', max_length=64)   
    def __str__(self):
        return self.name

class Cproduct(models.Model): 
    name = models.CharField(verbose_name='产品名称', max_length=64)   
    def __str__(self):
        return self.name
    
class Coperator(models.Model): 
    name = models.CharField(verbose_name='经办人', max_length=64)   
    def __str__(self):
        return self.name

class Customer(models.Model):
    """客户表"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)
    def __str__(self):
        return self.name

class Payment(models.Model):
    """付费记录"""
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer')
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now_add=True)

class Purchase(models.Model): 
    """采购模块"""
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)    
    name = models.CharField(verbose_name='供货商名称',max_length=64,null=True, blank=True)                
    product = models.CharField(verbose_name='采购产品名称', max_length=64,null=True, blank=True)                        
    number = models.FloatField(verbose_name='数量', default=0)
    price = models.FloatField(verbose_name='单价', default=0)
    money = models.FloatField(verbose_name='金额', default=0)
    payment = models.FloatField(verbose_name='支付款', default=0)
    balance = models.FloatField(verbose_name='结余款', default=0)    
    payment_method = models.CharField(verbose_name='支付方式', max_length=64, null=True, blank=True)
    operator = models.CharField(verbose_name='经办人', max_length=10,null=True, blank=True)
    note = models.CharField(verbose_name='备注', max_length=120, null=True, blank=True)
    def __str__(self):
        return self.name

class Delivery(models.Model): 
    """送货模块"""
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)    
    name = models.CharField(verbose_name='送货单位名称', max_length=64, null=True, blank=True)
    num = models.CharField(verbose_name='送货单号码', max_length=8, null=True, blank=True)
    customer = models.CharField(verbose_name='客户名称', max_length=64, null=True, blank=True)        
    product = models.CharField(verbose_name='送货产品名称', max_length=64, null=True, blank=True)
    number = models.FloatField(verbose_name='数量', default=0)
    price = models.FloatField(verbose_name='单价', default=0)
    money = models.FloatField(verbose_name='金额', default=0)
    operator = models.CharField(verbose_name='经办人', max_length=10, null=True, blank=True)
    note = models.CharField(verbose_name='备注', max_length=120, null=True, blank=True) 
    def __str__(self):
        return self.name

class Deliverycustomer(models.Model):
    name = models.CharField(verbose_name='客户名称', max_length=64)   
    def __str__(self):
        return self.name

class Deliveryproduct(models.Model):
    name = models.CharField(verbose_name='送货产品名称', max_length=64)   
    def __str__(self):
        return self.name

#---------------------------销售成本模块-------------------------------------- 
class Cost(models.Model): 
    """销售成本模型"""
    date = models.DateTimeField(default = timezone.now, null=True, blank=True) 
    name = models.CharField(verbose_name='客户名称', max_length=16, null=True, blank=True)   
    voucherno = models.CharField(verbose_name='凭证号', max_length=16, null=True, blank=True)
    abstract = models.CharField(verbose_name='摘要', max_length=256, null=True, blank=True)
    invoice = models.FloatField(verbose_name='开票额', default=0)        
    delivery = models.FloatField(verbose_name='发货额', default=0)
    cost_amount = models.FloatField(verbose_name='成本金额', default=0)
    pgross_profit = models.FloatField(verbose_name='毛利', default=0)
    meals = models.FloatField(verbose_name='餐费', default=0)
    travel_expenses = models.FloatField(verbose_name='差旅费', default=0)        
    gift = models.FloatField(verbose_name='礼品', default=0)    
    cash_gift = models.FloatField(verbose_name='礼金', default=0)
    recreation = models.FloatField(verbose_name='娱乐', default=0)
    car = models.FloatField(verbose_name='汽车费', default=0)
    subtotal0 = models.FloatField(verbose_name='小计0', default=0)
    cost_rate = models.FloatField(verbose_name='费用率', default=0)    
    return_freight = models.FloatField(verbose_name='退货运费', default=0)
    special_car = models.FloatField(verbose_name='专车费用', default=0)        
    customer_claims = models.FloatField(verbose_name='客诉赔款', default=0)
    payment_commission = models.FloatField(verbose_name='实际支付佣金', default=0)
    other = models.FloatField(verbose_name='其他', default=0)
    
    subtotal1 = models.FloatField(verbose_name='小计1', default=0)
    total_expenses = models.FloatField(verbose_name='费用合计', default=0)
    operator = models.CharField(verbose_name='经办人', max_length=10, null=True, blank=True)   
    def __str__(self):
        return self.name

#---------------------------应付账款--------------------------------------
class Copewith(models.Model): 
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)     
    name = models.CharField(verbose_name='客户名称', max_length=16, null=True, blank=True)
    receipt = models.CharField(verbose_name='收货单号码', max_length=16, null=True, blank=True)
    abstract = models.CharField(verbose_name='摘要', max_length=256, null=True, blank=True)
    payment = models.FloatField(verbose_name='付款', default=0) 
    number = models.FloatField(verbose_name='收货数量', default=0) 
    univalence = models.FloatField(verbose_name='单价', default=0)
    money = models.FloatField(verbose_name='金额', default=0)
    balance = models.FloatField(verbose_name='余额', default=0)
    note = models.CharField(verbose_name='备注', max_length=120, null=True, blank=True) 
    date1 = models.DateTimeField(default = timezone.now, null=True, blank=True) 
    Invoice_number = models.CharField(verbose_name='发票号码', max_length=16, null=True, blank=True)
    money1 = models.FloatField(verbose_name='金额1', default=0)
    owe_ticket = models.FloatField(verbose_name='欠票', default=0)
    operator = models.CharField(verbose_name='经办人', max_length=10, null=True, blank=True)  
    def __str__(self):
        return self.name

#应收账款
class Receivable(models.Model):
    date = models.DateTimeField(default = timezone.now, null=True, blank=True) 
    name = models.CharField(verbose_name='客户名称', max_length=256, default='请输入')
    receipt = models.CharField(verbose_name='送货单号码', max_length=16, default='请输入')
    abstract = models.CharField(verbose_name='摘要', max_length=256, default='请输入')     
    number = models.FloatField(verbose_name='送货数量', default=0) 
    univalence = models.FloatField(verbose_name='单价', default=0)
    money = models.FloatField(verbose_name='金额', default=0)
    collection = models.FloatField(verbose_name='收款', default=0)
    balance = models.FloatField(verbose_name='余额', default=0)
    note = models.CharField(verbose_name='备注', max_length=120, default='请输入') 
    date1 = models.DateTimeField(default = timezone.now, null=True, blank=True) 
    Invoice_number = models.CharField(verbose_name='发票号码', max_length=16, default='请输入')
    money1 = models.FloatField(verbose_name='金额1', default=0)
    owe_ticket = models.FloatField(verbose_name='欠客户票', default=0)
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')  
    def __str__(self):
        return self.name
    
#材料报表
class Materialreport(models.Model):
    date = models.DateTimeField(default = timezone.now, null=True, blank=True) 
    name = models.CharField(verbose_name='材料报表名称', max_length=256, default='请输入')
    material_name = models.CharField(verbose_name='材料名称', max_length=256, default='请输入')
    lastmonth_number = models.FloatField(verbose_name='上月结存数量', default=0)     
    lastmonth_univalence = models.FloatField(verbose_name='上月结存单价', default=0)
        
    lastmonth_money = models.FloatField(verbose_name='上月结存金额', default=0)    
    income_number = models.FloatField(verbose_name='收入数量', default=0)    
    income_univalence = models.FloatField(verbose_name='收入单价', default=0)    
    income_money = models.FloatField(verbose_name='收入金额', default=0)    
    weighting_number = models.FloatField(verbose_name='加权数量', default=0)
    
    weighting_univalence = models.FloatField(verbose_name='加权单价', default=0)      
    weighting_money = models.FloatField(verbose_name='加权金额', default=0)
    production_expenditure_number = models.FloatField(verbose_name='生产支出数量', default=0)      
    production_expenditure_univalence = models.FloatField(verbose_name='生产支出单价', default=0)      
    production_expenditure_money = models.FloatField(verbose_name='生产支出金额', default=0)
        
    material_expenditure_number = models.FloatField(verbose_name='材料支出数量', default=0)   
    material_expenditure_money = models.FloatField(verbose_name='材料支出金额', default=0)                 
    sale_number = models.FloatField(verbose_name='销售数量', default=0)               
    sale_money = models.FloatField(verbose_name='销售金额', default=0)                
    thismonth_number = models.FloatField(verbose_name='本月结存数量', default=0)
          
    thismonth_univalence = models.FloatField(verbose_name='本月结存单价', default=0)        
    thismonth_money = models.FloatField(verbose_name='本月结存金额', default=0)   
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')  
    def __str__(self):
        return self.name
    
# 产销存 报表
class Salesreport(models.Model):    
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)
     
    name = models.CharField(verbose_name='名称', max_length=256, default='请输入')
    product_name = models.CharField(verbose_name='产品名称', max_length=256, default='请输入')
    lastmonth_number = models.FloatField(verbose_name='上月结存数量', default=0)     
    lastmonth_univalence = models.FloatField(verbose_name='上月结存单价', default=0)        
    lastmonth_money = models.FloatField(verbose_name='上月结存金额', default=0) 
    
    thismonth_production_number = models.FloatField(verbose_name='本月生产数量', default=0)      
    thismonth_production_univalence = models.FloatField(verbose_name='本月生产单价', default=0)        
    thismonth_material = models.FloatField(verbose_name='本月生产材料', default=0)
    thismonth_artificial = models.FloatField(verbose_name='本月直接人工', default=0)    
    thismonth_cost = models.FloatField(verbose_name='本月制造费用', default=0)
    
    thismonth_production_money = models.FloatField(verbose_name='本月生产金额', default=0)   
    return_number = models.FloatField(verbose_name='本月退货数量', default=0)   
    return_money = models.FloatField(verbose_name='本月退货金额', default=0)      
    purchase_number = models.FloatField(verbose_name='本月购入数量', default=0)       
    purchase_money = models.FloatField(verbose_name='本月购入金额', default=0) 
             
    collaruse_number = models.FloatField(verbose_name='本月领用数量', default=0)   
    collaruse_money = models.FloatField(verbose_name='本月领用金额', default=0)          
    weighting_number = models.FloatField(verbose_name='加权数量', default=0)
    weighting_univalence = models.FloatField(verbose_name='加权单价', default=0)          
    weighting_money = models.FloatField(verbose_name='加权金额', default=0)
    
    goback_number = models.FloatField(verbose_name='本月退回数量', default=0) 
    goback_money = models.FloatField(verbose_name='本月退回金额', default=0)
    nullify_number = models.FloatField(verbose_name='本月作废数量', default=0) 
    nullify_money = models.FloatField(verbose_name='本月作废金额', default=0)    
    sample_sales_number = models.FloatField(verbose_name='本月样品销售数量', default=0)
         
    sample_sales_money = models.FloatField(verbose_name='本月样品销售金额', default=0)        
    thismonth_number = models.FloatField(verbose_name='本月结存数量', default=0)      
    thismonth_univalence = models.FloatField(verbose_name='本月结存单价', default=0)        
    thismonth_money = models.FloatField(verbose_name='本月结存金额', default=0)   
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')  
    def __str__(self):
        return self.name
    
# 领料汇总
class Picking(models.Model):    
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)     
    name = models.CharField(verbose_name='名称', max_length=256, default='请输入')
    receipt = models.CharField(verbose_name='领料单号码', max_length=16, default='请输入')
    material_name = models.CharField(verbose_name='材料名称及规格', max_length=64, default='请输入')    
    number = models.FloatField(verbose_name='数量', default=0)    
    univalence = models.FloatField(verbose_name='单价', default=0)          
    money = models.FloatField(verbose_name='金额', default=0)
    product_name = models.CharField(verbose_name='产品名称', max_length=256, default='请输入')
    remarks = models.CharField(verbose_name='备注', max_length=10, default='请输入') 
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')   
    def __str__(self):
        return self.name

# 成品入库    
class Warehousing(models.Model):    
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)     
    name = models.CharField(verbose_name='名称', max_length=256, default='请输入')    
    receipt = models.CharField(verbose_name='入库单号码', max_length=16, default='请输入')
    product_name = models.CharField(verbose_name='产品名称', max_length=256, default='请输入')
    number = models.FloatField(verbose_name='数量', default=0)    
    univalence = models.FloatField(verbose_name='单价', default=0)          
    money = models.FloatField(verbose_name='金额', default=0)    
    remarks = models.CharField(verbose_name='备注', max_length=10, default='请输入') 
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')   
    def __str__(self):
        return self.name

# 材料入库
class Materialstorage(models.Model):    
    date = models.DateTimeField(default = timezone.now, null=True, blank=True)     
    name = models.CharField(verbose_name='名称', max_length=256, default='请输入')    
    receipt = models.CharField(verbose_name='入库单号码', max_length=16, default='请输入')
    product_name = models.CharField(verbose_name='产品名称', max_length=256, default='请输入')
    number = models.FloatField(verbose_name='数量', default=0)    
    univalence = models.FloatField(verbose_name='单价', default=0)          
    money = models.FloatField(verbose_name='金额', default=0)    
    remarks = models.CharField(verbose_name='备注', max_length=10, default='请输入') 
    operator = models.CharField(verbose_name='经办人', max_length=10, default='请输入')   
    def __str__(self):
        return self.name
