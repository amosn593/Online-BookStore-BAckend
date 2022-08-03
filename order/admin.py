from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'place',
                    'created_at', 'paid_amount', 'mpesa_number', 'status')


admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)
