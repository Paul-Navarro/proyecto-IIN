# users/urls.py

from django.urls import path
from .views import editar_perfil
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('configurar-perfil/', editar_perfil, name='editar_perfil'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
]
