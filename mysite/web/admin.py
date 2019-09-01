from django.contrib import admin

# Register your models here.

from .models import Customer, Payment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):    
    list_display = ('id','name','age','email','company',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):    
    list_display = ('id', 'customer', 'money', 'create_time')