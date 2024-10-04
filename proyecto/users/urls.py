# users/urls.py

from django.urls import path
from .views import editar_perfil
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('configurar-perfil/', editar_perfil, name='editar_perfil'),
    path('notificacion/leida/<int:id>/', views.marcar_como_leida, name='marcar_como_leida'),
]
