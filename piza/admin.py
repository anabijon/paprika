from django.contrib import admin

# Register your models here.


from .models import Products, customers, category, sales_report, TestTable


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'status')
    search_fields = ('name', 'category')


admin.site.register(Products, ProductsAdmin)


class СustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'adress', 'status')
    search_fields = ('name', 'phone')

admin.site.register(customers, СustomersAdmin)

class CategorysAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name', 'comment', 'status')
    search_fields = ('cat_name', 'status')

admin.site.register(category, CategorysAdmin)

class Sales_reportsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'product_id', 'product_price', 'date' , 'delivery_address', 'status')
    search_fields = ('phone', 'delivery_address')

admin.site.register(sales_report, Sales_reportsAdmin)

class TestTableAdmin(admin.ModelAdmin):
    list_display = ('id_test', 'text')
    search_fields = ('id_test', 'text')

admin.site.register(TestTable, TestTableAdmin)