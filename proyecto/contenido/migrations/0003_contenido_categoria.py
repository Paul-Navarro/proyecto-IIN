# Generated by Django 5.1 on 2024-09-10 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0002_alter_categoria_codigo'),
        ('contenido', '0002_contenido_imagen_conte'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categorias.categoria'),
        ),
    ]
