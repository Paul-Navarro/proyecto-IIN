# Generated by Django 5.1 on 2024-09-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_create_admin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
