# Generated by Django 5.1 on 2024-09-25 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0008_rechazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='fecha_publicacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
