from django.contrib import admin

# Register your models here.

from .models import Customer, Payment, Purchase, Cname, Cproduct, Coperator
from .models import Delivery, Deliverycustomer, Deliveryproduct
from .models import Cost
from .models import Copewith,Receivable,Materialreport,Salesreport,Picking,Warehousing,Materialstorage

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):    
    list_display = ('id','name','age','email','company',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):    
    list_display = ('id', 'customer', 'money', 'create_time')
    
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):    
    list_display = ('id', 'date', 'name', 'product', 'number', 'price', 'money', 'payment', 'balance', 'payment_method','operator', 'note')
    
@admin.register(Cname)
class CnamerAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)

@admin.register(Cproduct)
class CproductAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)
    
@admin.register(Coperator)
class CoperatorAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)
    
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):    
    list_display = ('id','date', 'name','num','customer','product','number',\
         'price','money','operator','note',)

@admin.register(Deliverycustomer)
class DeliverycustomerAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)

@admin.register(Deliveryproduct)
class DeliveryproductAdmin(admin.ModelAdmin):    
    list_display = ('id','name',)

@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):    
    list_display = ('id',"date",'name',"voucherno","abstract","invoice","delivery",\
         "cost_amount","pgross_profit","meals","travel_expenses","gift",\
         "cash_gift","recreation","car","subtotal0","cost_rate",\
         "return_freight","special_car","customer_claims","payment_commission","other",\
         "subtotal1","total_expenses","operator")
            
@admin.register(Copewith)
class CopewithAdmin(admin.ModelAdmin):    
    list_display = ('id',"date","name","receipt","abstract","payment","number","univalence",\
         "money","balance","note","date1","Invoice_number",\
         "money1","owe_ticket","operator")    
    
@admin.register(Receivable)
class ReceivableAdmin(admin.ModelAdmin):    
    list_display = ('id',"date","name","receipt","abstract","number",\
            "univalence","money","collection","balance","note",\
            "date1","Invoice_number","money1","owe_ticket","operator")       
    
@admin.register(Materialreport)    
class ReceivableAdmin(admin.ModelAdmin):    
    list_display = ('id',"date","name","material_name",\
        "lastmonth_number","lastmonth_univalence","lastmonth_money",\
        "income_number","income_univalence","income_money",\
        "weighting_number","weighting_univalence","weighting_money",\
        "production_expenditure_number","production_expenditure_univalence","production_expenditure_money",\
        "material_expenditure_number","material_expenditure_money",\
        "sale_number","sale_money",\
        "thismonth_number","thismonth_univalence","thismonth_money","operator" )    

@admin.register(Salesreport)    
class SalesreportAdmin(admin.ModelAdmin):    
    list_display = ('id', "date", "name","product_name","lastmonth_number", "lastmonth_univalence","lastmonth_money",\
        "thismonth_production_number","thismonth_production_univalence","thismonth_material","thismonth_artificial","thismonth_cost",\
        "thismonth_production_money","return_number","return_money","purchase_number","purchase_money",\
        "collaruse_number","collaruse_money","weighting_number","weighting_univalence","weighting_money",\
        "goback_number","goback_money","nullify_number", "nullify_money","sample_sales_number",\
        "sample_sales_money","thismonth_number","thismonth_univalence","thismonth_money","operator",) 
    
@admin.register(Picking)    
class PickingAdmin(admin.ModelAdmin):    
    list_display = ('id', "date", "name","receipt","material_name","number",\
         "univalence","money","product_name","remarks","operator")

@admin.register(Warehousing)    
class WarehousingAdmin(admin.ModelAdmin):    
    list_display = ('id', "date", "name","receipt","product_name","number",\
         "univalence","money","remarks","operator")

@admin.register(Materialstorage)    
class MaterialstorageAdmin(admin.ModelAdmin):    
    list_display = ('id', "date", "name","receipt","product_name","number",\
         "univalence","money","remarks","operator")

      