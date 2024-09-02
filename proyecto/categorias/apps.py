from django.apps import AppConfig


class CategoriasConfig(AppConfig):
    """
    @class CategoriasConfig
    @extends AppConfig
    @description Configuración de la aplicación 'categorias'.
    Define el campo automático por defecto para las claves primarias en los modelos y especifica el nombre de la aplicación en el proyecto Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categorias'
