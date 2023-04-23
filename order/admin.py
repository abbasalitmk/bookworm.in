from django.contrib import admin
from .models import Payment, Order, OrderProduct, Razorpay


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'phone', 'city',
                    'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    list_per_page = 20


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Razorpay)
