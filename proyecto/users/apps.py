from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    @class UsersConfig
    @extends AppConfig
    @description Configuración de la aplicación 'users'. Define el campo automático por defecto y el nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Importa las señales al iniciar la aplicación
        import users.signals
