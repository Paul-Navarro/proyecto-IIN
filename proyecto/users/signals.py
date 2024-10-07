from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    '''
    @function assign_default_role
    @description Asigna el rol predeterminado de 'Suscriptor' a un usuario recién creado si no tiene ningún rol asignado.
    Este método se ejecuta automáticamente después de que un nuevo usuario sea guardado en la base de datos. Si el usuario
    no tiene roles asignados al momento de la creación, se le asigna el rol de 'Suscriptor' por defecto.
    
    @param sender {class} El modelo que envía la señal (en este caso, el modelo de usuario).
    @param instance {User} La instancia del usuario que ha sido creada o guardada.
    @param created {bool} Indica si la instancia del usuario fue recién creada.
    @param **kwargs {dict} Argumentos adicionales.
    '''
    if created:  # Solo se ejecuta cuando el usuario es creado
        if instance.roles.count() == 0:
            # Verificar si el usuario no tiene roles
            suscriptor_role = Role.objects.get(name='Suscriptor')
            instance.roles.add(suscriptor_role)
            instance.save()  # Guardar los cambios
