# Generated by Django 5.1 on 2024-11-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0026_historialcompra_metodo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='comparticiones_copiar_enlace',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='comparticiones_facebook',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='comparticiones_instagram',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='comparticiones_whatsapp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contenido',
            name='comparticiones_x',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
