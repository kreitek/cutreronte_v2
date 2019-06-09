from django.contrib import admin
from .models import RegistroMac


# admin.site.register(RegistroMac)
@admin.register(RegistroMac)
class RegistroMacAdmin(admin.ModelAdmin):
    list_display = ['dispositivo', 'estado', 'tiempo', ]
    list_filter = ['dispositivo', ]
    date_hierarchy = 'tiempo'
    ordering = ('-tiempo',)
    # readonly_fields = ['user']
