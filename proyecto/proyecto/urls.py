from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Importa las vistas desde el archivo 'views.py'
from users.views import (
    role_based_redirect,
    admin_dashboard,
    editor_dashboard,
    publicador_dashboard,
    suscriptor_dashboard,
    autor_dashboard,
    create_user,  # Vista para crear un usuario
    edit_user,    # Vista para editar un usuario
    delete_user,  # Vista para eliminar un usuario
    user_list,    # Vista para listar los usuarios
    home,
    role_based_redirect_choice,
)

urlpatterns = [
    # Redirige a la página principal
    path('', home, name='home'),

    # Redirige al dashboard según el rol
    path('dashboard/', role_based_redirect, name='role_based_redirect'),

    # Rutas para los diferentes dashboards según el rol
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('editor/dashboard/', editor_dashboard, name='editor_dashboard'),
    path('publicador/dashboard/', publicador_dashboard, name='publicador_dashboard'),
    path('suscriptor/dashboard/', suscriptor_dashboard, name='suscriptor_dashboard'),
    path('autor/dashboard/', autor_dashboard, name='autor_dashboard'),

    # Incluye las rutas de Django Allauth (autenticación)
    path('accounts/', include('allauth.urls')),

    # Rutas para la gestión de usuarios
    path('users/', user_list, name='user_list'),  # Lista de usuarios
    path('users/create/', create_user, name='create_user'),  # Crear un nuevo usuario
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),  # Editar un usuario existente
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),  # Eliminar un usuario existente

    # Rutas de categorías y contenido
    path('categorias/', include('categorias.urls')),  # Aquí incluyes las URLs de la app categorías
    path('contenido/', include('contenido.urls')),  # Ruta para la gestión de contenido

    # Rutas para seleccionar roles
    path('choose-role/', role_based_redirect, name='role_based_redirect'),
    path('choose-role/<str:role_name>/', role_based_redirect_choice, name='role_based_redirect_choice'),
]

# Para servir archivos media en modo DEBUG (desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
