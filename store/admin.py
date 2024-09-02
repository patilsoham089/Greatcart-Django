from django.contrib import admin
from store.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'slug')
    
admin.site.register(Product, ProductAdmin)