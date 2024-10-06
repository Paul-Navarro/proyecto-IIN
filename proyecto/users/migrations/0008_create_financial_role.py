from django.db import migrations

def create_financial_role_and_permissions(apps, schema_editor):
    Role = apps.get_model('users', 'Role')  # Modelo Role
    Permission = apps.get_model('auth', 'Permission')  # Permisos de Django

    # Crear el rol Financiero si no existe
    financiero_role, created = Role.objects.get_or_create(name='Financiero')

    # Obtener los permisos de ventas (asegurarse de que existan)
    financial_permissions = Permission.objects.filter(codename__in=[
        'view_sales',  # Permiso de ver ventas
        'filter_sales'  # Permiso de filtrar ventas
    ])

    # Asignar los permisos al rol Financiero
    if financial_permissions.exists():
        financiero_role.permissions.set(financial_permissions)
        financiero_role.save()
        print("Permisos asignados al rol Financiero.")
    else:
        print("No se encontraron permisos de ventas. Asegúrate de que los permisos existan.")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_venta'),  # Ajusta esta dependencia según tu estructura
    ]

    operations = [
        migrations.RunPython(create_financial_role_and_permissions),
    ]
