# Generated by Django 5.1 on 2024-10-20 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0003_categoria_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='precio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
