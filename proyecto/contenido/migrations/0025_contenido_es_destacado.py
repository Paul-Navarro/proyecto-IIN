# Generated by Django 5.1 on 2024-11-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0024_favorito'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='es_destacado',
            field=models.BooleanField(default=False),
        ),
    ]
