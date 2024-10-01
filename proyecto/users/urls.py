# users/urls.py

from django.urls import path
from .views import editar_perfil
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('configurar-perfil/', editar_perfil, name='editar_perfil'),
]
