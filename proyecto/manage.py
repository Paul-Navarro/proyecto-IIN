#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    @function main
    @description Configura las variables de entorno necesarias para el proyecto de Django y ejecuta 
    las tareas administrativas a través de la línea de comandos. Verifica que Django esté instalado 
    y correctamente configurado antes de ejecutar cualquier comando.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    

if __name__ == '__main__':
    main()
