from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


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
    





    








