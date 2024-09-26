from django.urls import path
from . import views

urlpatterns = [
    
    #Urls de los contenidos
    path('', views.contenido_list, name='contenido_list'),
    path('contenido/<int:pk>/', views.contenido_detail, name='contenido_detail'),
    
    path('contenido_editor/<int:pk>/', views.contenido_detail_editor, name='contenido_detail_editor'),
    path('contenido_publicador/<int:pk>/', views.contenido_detail_publicador, name='contenido_detail_publicador'),
    path('contenido_autor/<int:pk>/', views.contenido_detail_autor, name='contenido_detail_autor'),
    path('contenido/new/', views.contenido_create, name='contenido_create'),
    
    path('contenido/<int:pk>/edit/', views.contenido_update, name='contenido_update'),
    path('contenido/<int:pk>/edit_editor/', views.contenido_update_editor, name='contenido_update_editor'),
    
    path('contenido/<int:pk>/delete/', views.contenido_delete, name='contenido_delete'),
    path('contenido/<int:id>/', views.contenido_detail, name='contenido_detail'),
    
    path('contenido/cambiar-estado/<int:id_conte>/', views.contenido_cambiar_estado, name='contenido_cambiar_estado'),

    path('contenido/cambiar_estado/<int:id_conte>/', views.contenido_cambiar_estado_KANBAN, name='contenido_cambiar_estado_KANBAN'),
    
    #Urls del PUBLICADOR para administrar contenidos
     path('publicador/gestionar/', views.gestionar_contenido, name='gestionar_contenido'),
]

'''
@description Rutas de la aplicación 'contenido'. Define las rutas para listar, mostrar el detalle, crear, editar y eliminar contenido.
@routes
    @route {GET} / - Lista todos los contenidos. Utiliza la vista views.contenido_list.
    @route {GET} /contenido/<int:pk>/ - Muestra el detalle de un contenido específico. Utiliza la vista views.contenido_detail.
    @route {GET, POST} /contenido/new/ - Crea un nuevo contenido. Utiliza la vista views.contenido_create.
    @route {GET, POST} /contenido/<int:pk>/edit/ - Edita un contenido existente. Utiliza la vista views.contenido_update.
    @route {POST} /contenido/<int:pk>/delete/ - Elimina un contenido específico. Utiliza la vista views.contenido_delete.
'''