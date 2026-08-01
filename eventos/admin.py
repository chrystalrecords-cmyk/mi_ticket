from django.contrib import admin
from .models import Evento, Orden

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'precio')

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_comprador', 'email_comprador', 'evento', 'cantidad', 'monto_total', 'estado_pago', 'fecha_creacion')
    list_filter = ('estado_pago', 'fecha_creacion', 'evento')
    search_fields = ('nombre_comprador', 'email_comprador', 'id')