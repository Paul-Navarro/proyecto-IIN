from django.urls import path
from . import views

urlpatterns = [
    path('', views.contenido_list, name='contenido_list'),
    path('contenido/<int:pk>/', views.contenido_detail, name='contenido_detail'),
    path('contenido/new/', views.contenido_create, name='contenido_create'),
    path('contenido/<int:pk>/edit/', views.contenido_update, name='contenido_update'),
    path('contenido/<int:pk>/delete/', views.contenido_delete, name='contenido_delete'),
]
