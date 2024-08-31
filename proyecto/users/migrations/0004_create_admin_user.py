from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'CustomUser')
    Role = apps.get_model('users', 'Role')

    # Crear el usuario admin
    admin_user, created = User.objects.get_or_create(
        username='adminuser',
        defaults={
            'email': 'paulnavarro1912@gmail.com',
            'password': make_password('leti1168'),  
            'is_active': True,
            'is_staff': True,  
        }
    )

    if created:
        # Obtener el rol de Admin y asignarlo
        admin_role = Role.objects.get(name='Admin')
        admin_user.roles.add(admin_role)
        admin_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_assign_permissions_to_roles'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
