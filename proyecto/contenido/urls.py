from django.urls import path
from . import views
from .views import suscripciones_view, comprar_suscripcion, contacto

urlpatterns = [
    
    #Urls de los contenidos
    path('', views.contenido_list, name='contenido_list'),
    path('contenido/<int:pk>/', views.contenido_detail, name='contenido_detail'),
    
    path('contenido_admin', views.administrador_KANBAN, name='administrador_KANBAN'),
    
    
    path('contenido_editor/<int:pk>/', views.contenido_detail_editor, name='contenido_detail_editor'),
    path('contenido_publicador/<int:pk>/', views.contenido_detail_publicador, name='contenido_detail_publicador'),
    path('contenido_autor/<int:pk>/', views.contenido_detail_autor, name='contenido_detail_autor'),
    path('contenido/new/', views.contenido_create, name='contenido_create'),
    
    path('contenido/<int:pk>/version/<int:version_num>/', views.contenido_version_detail, name='contenido_version_detail'),
    
    path('contenido/<int:pk>/edit/', views.contenido_update, name='contenido_update'),
    path('contenido/<int:pk>/edit_editor/', views.contenido_update_editor, name='contenido_update_editor'),
    
    path('contenido/<int:pk>/delete/', views.contenido_delete, name='contenido_delete'),
    path('contenido_admin/<int:pk>/delete/', views.contenido_delete_admin, name='contenido_delete_admin'),
    
    path('contenido/<int:id>/', views.contenido_detail, name='contenido_detail'),
    
    path('contenido/cambiar-estado/<int:id_conte>/', views.contenido_cambiar_estado, name='contenido_cambiar_estado'),

    path('contenido/cambiar_estado/<int:id_conte>/', views.contenido_cambiar_estado_KANBAN, name='contenido_cambiar_estado_KANBAN'),
    
    #Urls del PUBLICADOR para administrar contenidos
     path('publicador/gestionar/', views.gestionar_contenido, name='gestionar_contenido'),
     
     
     path('contenido/<int:id_conte>/like/', views.like_contenido, name='like_contenido'),
     path('contenido/<int:id_conte>/unlike/', views.unlike_contenido, name='unlike_contenido'),

    #Url para suscripcion
    path('suscripciones/', views.suscripciones_view, name='suscripciones'),

    #Url para suscripppcion
    path('suscripciones/', suscripciones_view, name='suscripciones_view'),
    path('comprar_suscripcion/', comprar_suscripcion, name='comprar_suscripcion'),
    path('success/', views.suscripcion_exitosa, name='suscripcion_exitosa'),
    path('cancel/', views.suscripcion_cancelada, name='suscripcion_cancelada'),
    path('contact_us/', views.contact_us, name='contact_us'),
    #url para desuscripcion
    path('desuscribir/<int:categoria_id>/', views.desuscribir_categoria, name='desuscribir_categoria'),
    path('contacto/', contacto, name='contacto'),

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