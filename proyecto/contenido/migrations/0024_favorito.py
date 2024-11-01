# Generated by Django 5.1 on 2024-11-01 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0023_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('contenido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos', to='contenido.contenido')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'contenido')},
            },
        ),
    ]