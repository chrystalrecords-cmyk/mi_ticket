import mercadopago
import qrcode
import io
import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .models import Evento, Orden

MERCADOPAGO_ACCESS_TOKEN = "APP_USR-830626259037279-073016-c6b27d73bd0e4725b02c4628f0770d24-374749734"

def lista_eventos(request):
    query = request.GET.get('q')
    if query:
        eventos = Evento.objects.filter(
            Q(nombre__icontains=query) | Q(lugar__icontains=query)
        )
    else:
        eventos = Evento.objects.all()
    return render(request, 'eventos/lista.html', {'eventos': eventos})
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        nombre_comprador = request.POST.get('nombre')
        email_comprador = request.POST.get('email')
        cantidad = int(request.POST.get('cantidad', 1))
        monto_total = float(evento.precio) * cantidad

        # 1. Crear la orden dinamica para el evento seleccionado
        orden = Orden.objects.create(
            evento=evento,
            nombre_comprador=nombre_comprador,
            email_comprador=email_comprador,
            cantidad=cantidad,
            monto_total=monto_total,
            estado_pago='PENDIENTE'
        )

        # 2. Configurar Mercado Pago dinamico segun el evento y su precio
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        preference_data = {
            "items": [
                {
                    "title": f"Entrada(s) para {evento.nombre}",
                    "quantity": cantidad,
                    "unit_price": float(evento.precio),
                    "currency_id": "ARS",
                }
            ],
            "payer": {
                "name": nombre_comprador,
                "email": email_comprador,
            },
            "external_reference": str(orden.id),
            "notification_url": "https://mi-ticket.onrender.com/webhook/",
            "back_urls": {
                "success": request.build_absolute_uri(f'/pago-exitoso/{orden.id}/'),
                "failure": request.build_absolute_uri(f'/pago-fallido/{orden.id}/'),
                "pending": request.build_absolute_uri(f'/pago-pendiente/{orden.id}/'),
            },
            "auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        if "id" in preference:
            orden.mercadopago_preference_id = preference["id"]
            orden.save()

        link_pago_dinamico = preference.get("init_point") or preference.get("sandbox_init_point")
        
        if link_pago_dinamico:
            return redirect(link_pago_dinamico)
        else:
            print("ERROR MERCADO PAGO:", preference_response)
            
    return render(request, 'eventos/detalle.html', {'evento': evento})

def ver_ticket(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)

    contenido_qr = f"TICKET-{orden.id}-{orden.email_comprador}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(contenido_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'eventos/ticket.html', {
        'orden': orden,
        'qr_code': qr_base64
    })

def pago_exitoso(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    orden.estado_pago = 'APROBADO'
    orden.save()
    return render(request, 'eventos/pago_exitoso.html', {'orden': orden})

def pago_fallido(request, orden_id):
    orden = Orden.objects.filter(id=orden_id).first()
    if orden:
        orden.estado_pago = 'RECHAZADO'
        orden.save()
    return render(request, 'eventos/pago_fallido.html', {'orden': orden})

def pago_pendiente(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    orden.estado_pago = 'PENDIENTE'
    orden.save()
    return render(request, 'eventos/pago_pendiente.html', {'orden': orden})
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def dashboard_organizador(request):
    # Si es superusuario ve todo; si es organizador solo ve sus eventos
    if request.user.is_superuser:
        eventos = Evento.objects.all()
        ordenes_pagadas = Orden.objects.filter(estado_pago='APROBADO')
    else:
        eventos = Evento.objects.filter(organizador=request.user)
        ordenes_pagadas = Orden.objects.filter(evento__organizador=request.user, estado_pago='APROBADO')
    
    total_recaudado = ordenes_pagadas.aggregate(Sum('monto_total'))['monto_total__sum'] or 0
    total_entradas = ordenes_pagadas.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    
    context = {
        'eventos': eventos,
        'ordenes': ordenes_pagadas,
        'total_recaudado': total_recaudado,
        'total_entradas': total_entradas,
    }
    return render(request, 'eventos/dashboard.html', context)