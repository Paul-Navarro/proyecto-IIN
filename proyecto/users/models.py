from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
"""
class CustomUser(AbstractUser):
    '''
    Modelo personalizado de usuario que extiende el modelo de usuario predeterminado de Django (AbstractUser).
    Este modelo permite agregar campos adicionales y personalizar la relación con grupos y permisos.
    '''

    # Campo de correo electrónico único para cada usuario.
    email = models.EmailField(unique=True)

    # Campos booleanos para definir roles específicos del usuario.
    is_subscriber = models.BooleanField(default=False)  # Indica si el usuario es un suscriptor.
    is_editor = models.BooleanField(default=False)      # Indica si el usuario es un editor.
    is_publisher = models.BooleanField(default=False)   # Indica si el usuario es un publicador.
    is_admin = models.BooleanField(default=False)       # Indica si el usuario es un administrador.

    # Relación de muchos a muchos con el modelo Group de Django.
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Nombre de la relación inversa desde Group hacia CustomUser.
        blank=True,                     # Permite que este campo sea opcional.
        help_text='The groups this user belongs to.',  # Texto de ayuda para la interfaz de administración.
        verbose_name='groups',          # Nombre legible para la interfaz de administración.
        related_query_name='customuser', # Nombre para las consultas relacionadas desde Group hacia CustomUser.
    )

    # Relación de muchos a muchos con el modelo Permission de Django.
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Nombre de la relación inversa desde Permission hacia CustomUser.
        blank=True,                                 # Permite que este campo sea opcional.
        help_text='Specific permissions for this user.',  # Texto de ayuda para la interfaz de administración.
        verbose_name='user permissions',            # Nombre legible para la interfaz de administración.
        related_query_name='customuser',            # Nombre para las consultas relacionadas desde Permission hacia CustomUser.
    )

    def __str__(self):
        '''
        Devuelve una representación en cadena del usuario, mostrando su nombre de usuario.
        Esto es útil en la interfaz administrativa y en otros contextos donde se necesite una representación legible.
        '''
        return self.username
"""

#clase para los roles
class Role(models.Model):
    """Modelo de Rol para gestionar roles dinámicos."""
    name = models.CharField(max_length=50, unique=True)  # Nombre del rol
    permissions = models.ManyToManyField(Permission, blank=True)  # Permisos asociados al rol

    def __str__(self):
        return self.name

#clase de usuario modificado
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')  # Relación con roles

    def __str__(self):
        return self.username

    def has_role(self, role_name):
        """
        Comprueba si el usuario tiene un rol específico.
        """
        return self.roles.filter(name=role_name).exists()

    def get_permissions(self):
        """
        Obtiene todos los permisos asociados a los roles del usuario.
        """
        permissions = super().get_user_permissions()
        for role in self.roles.all():
            permissions |= set(role.permissions.values_list('codename', flat=True))
        return permissions
    





    








