from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class ServiceAdmin(admin.ModelAdmin):

    # 🔹 Admin paneldan saqlayotganda requestni modelga uzatyapmiz
    def save_model(self, request, obj, form, change):
        obj.save(request=request)

admin.site.register(OrderItem)