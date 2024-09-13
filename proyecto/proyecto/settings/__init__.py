import os

if os.getenv('DJANGO_ENV') == 'produccion':
    from .produccion import *
else:
    from .desarrollo import *