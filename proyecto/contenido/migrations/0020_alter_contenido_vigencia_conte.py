# Generated by Django 5.1 on 2024-10-06 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0019_contenido_fecha_vigencia_contenido_vigencia_conte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='vigencia_conte',
            field=models.BooleanField(default=False),
        ),
    ]