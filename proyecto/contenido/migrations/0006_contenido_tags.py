# Generated by Django 5.1 on 2024-09-13 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0005_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='tags',
            field=models.ManyToManyField(blank=True, to='contenido.tag'),
        ),
    ]
