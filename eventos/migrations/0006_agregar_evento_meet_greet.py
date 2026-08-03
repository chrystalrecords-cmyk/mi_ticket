from django.db import migrations

def crear_evento_mg(apps, schema_editor):
    Evento = apps.get_model('eventos', 'Evento')
    # Creamos el evento si no existe
    Evento.objects.get_or_create(
        nombre="Jay Aston's Gene Loves Jezebel - Show + Meet & Greet",
        defaults={
            'descripcion': "Entrada Show + Meet & Greet exclusivo.",
            'fecha': "2026-11-07 21:00:00",
            'lugar': "Auditorio Beethoven (Av. Santa Fe 1452, Recoleta)",
            'precio': 180000.00,
            'capacidad': 60,
        }
    )

def eliminar_evento_mg(apps, schema_editor):
    Evento = apps.get_model('eventos', 'Evento')
    Evento.objects.filter(nombre="Jay Aston's Gene Loves Jezebel - Show + Meet & Greet").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_alter_orden_email_comprador_alter_orden_evento_and_more'), # Asegurate que apunte a tu última migración
    ]

    operations = [
        migrations.RunPython(crear_evento_mg, eliminar_evento_mg),
    ]