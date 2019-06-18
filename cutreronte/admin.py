from django.contrib import admin
from django.db.models import Count

from .models import Dispositivo, Rfid, Usuario


class RfidInline(admin.TabularInline):
    model = Rfid
    extra = 0
    # exclude = ['numero', ]
    can_delete = True

    # def get_max_num(self, request, obj=None, **kwargs):
    #     return obj.slotentrada_set.count()


class DispositivoInline(admin.TabularInline):
    model = Dispositivo
    extra = 0
    can_delete = True


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'estado', 'last_seen', 'n_rfids', 'n_dispositivos', ]
    list_filter = ['estado']
    ordering = ["-last_seen", ]
    inlines = [RfidInline, DispositivoInline]

    # readonly_fields = ['user', ]

    def n_rfids(self, instancia):
        return Rfid.objects.filter(usuario__id=instancia.id).count()

    def n_dispositivos(self, instancia):
        return Dispositivo.objects.filter(usuario__id=instancia.id).count()


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ['mac', 'usuario', ]
    search_fields = ['mac', ]


@admin.register(Rfid)
class RfidAdmin(admin.ModelAdmin):
    list_display = ['rfid', 'usuario', ]
    search_fields = ['rfid', ]
