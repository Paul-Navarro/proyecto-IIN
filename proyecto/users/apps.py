from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    @class ContenidoConfig
    @extends AppConfig
    @description Configuración de la aplicación 'contenido'. Define el campo automático por defecto y el nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
