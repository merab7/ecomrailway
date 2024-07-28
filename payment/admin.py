from django.contrib import admin
from .models import ShippingAddress, Order, Order_item, CuponCode
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(CuponCode)

#make order item inline
class OrderItemInline(admin.StackedInline):
    model = Order_item
    extra = 0

#extend order model

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date']
    inlines = [OrderItemInline]

#unregister order
admin.site.unregister(Order)

#re_register ORDER ADN ORDERadmin
admin.site.register(Order, OrderAdmin)