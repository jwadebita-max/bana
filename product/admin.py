from django.contrib import admin
from .models import FoodItem

# Register your models here.
admin.site.register(FoodItem)


admin.site.site_header = "BENNA Control Panel"
admin.site.site_title = "BENNA Admin"
admin.site.index_title = "Welcome to BENNA Management"

# ربط ملف الـ CSS الخاص بالأدمن
class Media:
    css = {
        'all': ('css/custom_admin.css',)
    }

admin.site.Media = Media

