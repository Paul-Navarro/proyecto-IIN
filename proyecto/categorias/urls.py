from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_categorias, name='listar_categorias'),
    path('crear/', views.crear_categoria, name='crear_categoria'),  # Añade esta línea para la vista de creación
    path('editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),  # También podrías añadir la URL para editar
    path('eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),  # Y la URL para eliminar
]
