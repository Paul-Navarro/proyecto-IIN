# Generated by Django 5.1 on 2024-10-04 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0013_versioncontenido'),
    ]

    operations = [
        migrations.CreateModel(
            name='CambioBorrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cambios_borrador', to='contenido.contenido')),
            ],
        ),
    ]
