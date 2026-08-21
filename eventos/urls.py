from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('ticket/<int:orden_id>/', views.ver_ticket, name='ver_ticket'),
    path('pago-exitoso/<int:orden_id>/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/<int:orden_id>/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/<int:orden_id>/', views.pago_pendiente, name='pago_pendiente'),
    path('panel/', views.dashboard_organizador, name='dashboard'),
]