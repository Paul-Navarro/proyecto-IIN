# Generated by Django 5.1 on 2024-09-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='imagen_conte',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes_contenido/'),
        ),
    ]