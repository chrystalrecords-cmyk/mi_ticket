from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('ticket/<int:orden_id>/', views.ver_ticket, name='ver_ticket'),
    path('validar/<int:orden_id>/', views.validar_ticket, name='validar_ticket'),
    path('pago-exitoso/<int:orden_id>/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/<int:orden_id>/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/<int:orden_id>/', views.pago_pendiente, name='pago_pendiente'),
    path('panel/', views.dashboard_organizador, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='eventos/login.html', redirect_authenticated_user=True), name='login'),
    path('registro/', views.registro_organizador, name='registro'),
    path('evento/<int:evento_id>/ver/', views.ver_evento_online, name='ver_evento_online'),
    path('store/', views.store_view, name='store'),
    path('tienda/exito/', views.tienda_exito, name='tienda_exito'),
    path('tienda/fallo/', views.tienda_fallo, name='tienda_fallo'),
]