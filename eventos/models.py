from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    organizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='flyers/', blank=True, null=True)
    link_video = models.URLField(max_length=500, blank=True, null=True, help_text="Link embed de YouTube o Vimeo")
    TIPO_CONTENIDO = (
        ('stream', 'Stream en Vivo'),
        ('pelicula', 'Película'),
        ('show', 'Show / Concierto en Vivo'),
    )
    tipo_contenido = models.CharField(max_length=10, choices=TIPO_CONTENIDO, default='pelicula')
    MODO_ACCESO = (
        ('PRESENCIAL', 'Presencial (con QR en puerta)'),
        ('ON_DEMAND', 'On Demand (Disponible siempre)'),
        ('FUNCION', 'Función Programada (Fecha y hora fija)'),
    )
    modo_acceso = models.CharField(max_length=20, choices=MODO_ACCESO, default='PRESENCIAL')
    # Nuevos campos de conversión internacional
    price_in_ars = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency_target = models.CharField(max_length=3, default='ARS')
    
    COUNTRY_CURRENCY_CHOICES = [
        ('ARS', 'Argentina (ARS) - 🇦🇷'),
        ('EUR', 'España (EUR) - 🇪🇸'),
        ('EUR', 'Francia (EUR) - 🇫🇷'),
        ('EUR', 'Italia (EUR) - 🇮🇹'),
        ('USD', 'Estados Unidos / Ecuador / Panamá (USD) - 🇺🇸/🇪🇨/🇵🇦'),
        ('CAD', 'Canadá (CAD) - 🇨🇦'),
        ('MXN', 'México (MXN) - 🇲🇽'),
        ('PYG', 'Paraguay (PYG) - 🇵🇾'),
        ('CLP', 'Chile (CLP) - 🇨🇱'),
        ('UYU', 'Uruguay (UYU) - 🇺🇾'),
        ('BRL', 'Brasil (BRL) - 🇧🇷'),
        ('AWG', 'Aruba (AWG) - 🇦🇼'),
        ('DOP', 'República Dominicana (DOP) - 🇩🇴'),
        ('TTD', 'Trinidad y Tobago (TTD) - 🇹🇹'),
        ('BZD', 'Dólar beliceño (BZD) - 🇧🇿'),
        ('GYD', 'Dólar guyanés (GYD) - 🇬🇾'),
        ('SRD', 'Dólar surinamés (SRD) - 🇸🇷'),
    ]
    country_market = models.CharField(max_length=50, choices=COUNTRY_CURRENCY_CHOICES, default='ARS')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)

    @property
    def formatted_visual_price(self):
        converted_value = self.price_in_ars * self.exchange_rate
        return f"{self.currency_target} {converted_value:,.0f}"
    def __str__(self):
        return self.nombre

class Orden(models.Model):
    ESTADOS_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nombre_comprador = models.CharField(max_length=100)
    email_comprador = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='PENDIENTE')
    mercadopago_preference_id = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden {self.id} - {self.evento.nombre} ({self.nombre_comprador})"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    from django.db import models

class BannerPromocional(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del Banner")
    imagen = models.ImageField(upload_to='banners/', verbose_name="Imagen del Banner")
    enlace = models.URLField(blank=True, null=True, verbose_name="Enlace (opcional)")
    activo = models.BooleanField(default=True, verbose_name="¿Mostrar en la página?")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de aparición")

    def __str__(self):
        return self.titulo