from django.contrib import admin
from .models import RegistroMac


# admin.site.register(RegistroMac)
@admin.register(RegistroMac)
class RegistroMacAdmin(admin.ModelAdmin):
    list_display = ['mac', 'estado', 'tiempo', ]
    list_filter = ['mac', ]
    date_hierarchy = 'tiempo'
    ordering = ('-tiempo',)
    # readonly_fields = ['user']
