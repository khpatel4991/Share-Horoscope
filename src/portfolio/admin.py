from django.contrib import admin

# Register your models here.

from .models import Stock

class StockAdmin(admin.ModelAdmin):
    class Meta:
        model = Stock
        
admin.site.register(Stock, StockAdmin)  #Registered a model in Admin
