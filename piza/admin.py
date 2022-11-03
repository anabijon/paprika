from django.contrib import admin

# Register your models here.


from .models import Products, customers, category, sales_report, TestTable, orders, OrderItem, ProductItem, contact_info, DeliveryInfo

class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    raw_id_fields = ['product']

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status')
    search_fields = ('name', 'category')
    inlines = [ProductItemAdmin]


admin.site.register(Products, ProductsAdmin)


class СustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'adress', 'status')
    search_fields = ('name', 'phone')

admin.site.register(customers, СustomersAdmin)

class CategorysAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'position', 'comment', 'status')
    search_fields = ('cat_name', 'status')

admin.site.register(category, CategorysAdmin)

class Sales_reportsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'product_id', 'product_price', 'date' , 'delivery_address', 'status')
    search_fields = ('phone', 'delivery_address')

admin.site.register(sales_report, Sales_reportsAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class DeliveryAdmin(admin.TabularInline):
    model = DeliveryInfo
    raw_id_fields = ['order']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('phone', 'date', 'order_id')
    search_fields = ('phone', 'delivery_address')
    list_filter = ['paid', 'date']
    inlines = [DeliveryAdmin]

admin.site.register(orders, OrdersAdmin)

class ContacInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'adress')
    search_fields = ('phone', 'name')

admin.site.register(contact_info, ContacInfoAdmin)



