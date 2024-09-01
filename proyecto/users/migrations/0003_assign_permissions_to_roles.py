#Con este archivo al hacer la migracion, carga los roles y permisos a la base de datos

from django.db import migrations

def create_roles_and_assign_permissions(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Permission = apps.get_model('auth', 'Permission')

    # Crear roles si no existen
    suscriptor_role, _ = Role.objects.get_or_create(name='Suscriptor')
    editor_role, _ = Role.objects.get_or_create(name='Editor')
    publicador_role, _ = Role.objects.get_or_create(name='Publicador')
    admin_role, _ = Role.objects.get_or_create(name='Admin')

    # Obtener permisos de contenido
    content_permissions = Permission.objects.filter(codename__in=[
        'view_content', 'add_content', 'change_content', 'delete_content'
    ])

    # Obtener permisos de usuario
    user_permissions = Permission.objects.filter(codename__in=[
        'view_user', 'add_user', 'change_user', 'delete_user'
    ])

    # Asignar permisos específicos a cada rol
    suscriptor_role.permissions.set(content_permissions.filter(codename='view_content'))

    editor_role.permissions.set(content_permissions)

    publicador_role.permissions.set(list(content_permissions) + list(user_permissions.filter(codename='view_user')))

    admin_role.permissions.set(list(content_permissions) + list(user_permissions))

    # Guardar cambios
    suscriptor_role.save()
    editor_role.save()
    publicador_role.save()
    admin_role.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_is_admin_and_more'),  # Asegúrate de ajustar esta dependencia si es necesario
    ]

    operations = [
        migrations.RunPython(create_roles_and_assign_permissions),
    ]
