from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'food_item', 'dish_counter', 'request_type', 'created_at')
    list_filter = ('request_type', 'created_at')
    search_fields = ('full_name', 'phone_number', 'delivery_address')


admin.site.site_header = "BENNA Control Panel"
admin.site.site_title = "BENNA Admin"
admin.site.index_title = "Welcome to BENNA Management"

# ربط ملف الـ CSS الخاص بالأدمن
class Media:
    css = {
        'all': ('css/custom_admin.css',)
    }

admin.site.Media = Media
