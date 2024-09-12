from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """
    Asigna el rol 'Suscriptor' a un usuario recién creado si no tiene roles asignados.
    """
    if created:  # Solo se ejecuta cuando el usuario es creado
        if instance.roles.count() == 0:
            # Verificar si el usuario no tiene roles
            suscriptor_role = Role.objects.get(name='Suscriptor')
            instance.roles.add(suscriptor_role)
            instance.save()  # Guardar los cambios
