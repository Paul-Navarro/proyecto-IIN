from django.urls import path
from . import views
from .views import enviar_informe, suscripciones_view, comprar_suscripcion, contacto, historial_compras_view, ver_estadisticas

from contenido.views import VentaListView

urlpatterns = [
    
    #Urls de los contenidos
    path('', views.contenido_list, name='contenido_list'),
    path('contenido/<int:pk>/', views.contenido_detail, name='contenido_detail'),
    path('<int:pk>/rate/', views.contenido_detail, name='rate_contenido'),#para la calificación de las estrellas
    path('contenido_admin', views.administrador_KANBAN, name='administrador_KANBAN'),
    
    path('contenido/seleccionar_version/<int:pk>/<int:version_id>/', views.seleccionar_version, name='seleccionar_version'),

    
    path('contenido_editor/<int:pk>/', views.contenido_detail_editor, name='contenido_detail_editor'),
    path('contenido_publicador/<int:pk>/', views.contenido_detail_publicador, name='contenido_detail_publicador'),
    path('contenido_autor/<int:pk>/', views.contenido_detail_autor, name='contenido_detail_autor'),
    path('contenido_autor_FLAG/<int:pk>/', views.contenido_detail_autor_FLAG, name='contenido_detail_autor_FLAG'),
    
    path('contenido/new/', views.contenido_create, name='contenido_create'),
    
    path('contenido/<int:pk>/version/<int:version_num>/', views.contenido_version_detail, name='contenido_version_detail'),
    
    path('contenido/<int:pk>/edit/', views.contenido_update, name='contenido_update'),
    path('contenido/<int:pk>/edit_editor/', views.contenido_update_editor, name='contenido_update_editor'),
    
    path('contenido/<int:pk>/delete/', views.contenido_delete, name='contenido_delete'),
    path('contenido_admin/<int:pk>/delete/', views.contenido_delete_admin, name='contenido_delete_admin'),
    
    path('contenido/<int:id>/', views.contenido_detail, name='contenido_detail'),
    
    path('contenido/cambiar-estado/<int:id_conte>/', views.contenido_cambiar_estado, name='contenido_cambiar_estado'),

    path('contenido/cambiar_estado/<int:id_conte>/', views.contenido_cambiar_estado_KANBAN, name='contenido_cambiar_estado_KANBAN'),
    
    path('contenido/version/<int:version_id>/edit/', views.contenido_update_version, name='contenido_update_version'),
    
    
    
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
    path('suscripciones/no-pagadas/', views.suscribirse_no_pagadas, name='suscribirse_no_pagadas'),
    #Url para reporte
    path('contenido/<int:contenido_id_conte>/reportar/', views.reportar_contenido, name='reportar_contenido'),
    path('admin/reportes/', views.ver_reportes, name='ver_reportes'),  # Ruta para ver los reportes
    path('historial-compras/', historial_compras_view, name='historial_compras'),
    path('ventas/', VentaListView.as_view(), name='venta_list'),
    
    path('contenido/registro/<int:pk>/', views.contenido_registro, name='contenido_registro'),   
    
    path('contenido/asignar_fecha_publicacion/<int:pk>/', views.asignar_fecha_publicacion, name='asignar_fecha_publicacion'),

    path('estadisticas/', ver_estadisticas, name='ver_estadisticas'),
    path('enviar-informe/', enviar_informe, name='enviar_informe'),  # Ruta para enviar el informe por correo
    
    path('inhabilitar/<int:pk>/', views.inhabilitar_contenido, name='inhabilitar_contenido'),
    
    path('contenido/<int:contenido_id>/agregar_favorito/', views.agregar_favorito, name='agregar_favorito'),
    path('contenido/<int:contenido_id>/eliminar_favorito/', views.eliminar_favorito, name='eliminar_favorito'),
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('contenido/<int:pk>/toggle_destacado/', views.toggle_destacado, name='contenido_toggle_destacado'),

]

'''
    @description Rutas de la aplicación 'contenido'. Define las rutas para listar, mostrar el detalle, crear, editar y eliminar contenido.
    @routes
        @route {GET} / - Lista todos los contenidos. Utiliza la vista views.contenido_list.
        @route {GET} /contenido/<int:pk>/ - Muestra el detalle de un contenido específico. Utiliza la vista views.contenido_detail.
        @route {GET} /contenido_admin/ - Interfaz KANBAN para que los administradores gestionen contenidos. Utiliza la vista views.administrador_KANBAN.
        @route {GET} /contenido/seleccionar_version/<int:pk>/<int:version_id>/ - Selecciona una versión específica de un contenido. Utiliza la vista views.seleccionar_version.
        @route {GET} /contenido_autor/<int:pk>/ - Muestra el detalle de un contenido para el autor. Utiliza la vista views.contenido_detail_autor.
        @route {GET} /contenido/new/ - Crea un nuevo contenido. Utiliza la vista views.contenido_create.
        @route {GET} /contenido/<int:pk>/version/<int:version_num>/ - Muestra los detalles de una versión específica del contenido. Utiliza la vista views.contenido_version_detail.
        @route {GET, POST} /contenido/<int:pk>/edit/ - Edita un contenido existente. Utiliza la vista views.contenido_update.
        @route {GET, POST} /contenido/<int:pk>/edit_editor/ - Edita un contenido específico para los editores. Utiliza la vista views.contenido_update_editor.
        @route {POST} /contenido/<int:pk>/delete/ - Elimina un contenido específico. Utiliza la vista views.contenido_delete.
        @route {POST} /contenido_admin/<int:pk>/delete/ - Elimina un contenido específico desde la administración. Utiliza la vista views.contenido_delete_admin.
        @route {POST} /contenido/cambiar-estado/<int:id_conte>/ - Cambia el estado de un contenido. Utiliza la vista views.contenido_cambiar_estado.
        @route {POST} /contenido/cambiar_estado_KANBAN/<int:id_conte>/ - Cambia el estado de un contenido desde la interfaz KANBAN. Utiliza la vista views.contenido_cambiar_estado_KANBAN.
        @route {GET} /publicador/gestionar/ - Interfaz de gestión de contenidos para el publicador. Utiliza la vista views.gestionar_contenido.
        @route {POST} /contenido/<int:id_conte>/like/ - Añade un like a un contenido. Utiliza la vista views.like_contenido.
        @route {POST} /contenido/<int:id_conte>/unlike/ - Añade un unlike a un contenido. Utiliza la vista views.unlike_contenido.
        @route {GET} /suscripciones/ - Muestra las suscripciones del usuario. Utiliza la vista views.suscripciones_view.
        @route {POST} /comprar_suscripcion/ - Compra una suscripción. Utiliza la vista views.comprar_suscripcion.
        @route {GET} /success/ - Indica una suscripción exitosa. Utiliza la vista views.suscripcion_exitosa.
        @route {GET} /cancel/ - Indica una suscripción cancelada. Utiliza la vista views.suscripcion_cancelada.
        @route {GET, POST} /contact_us/ - Muestra un formulario de contacto. Utiliza la vista views.contact_us.
        @route {POST} /desuscribir/<int:categoria_id>/ - Permite al usuario desuscribirse de una categoría. Utiliza la vista views.desuscribir_categoria.
        @route {GET} /suscripciones/no-pagadas/ - Muestra suscripciones que no han sido pagadas. Utiliza la vista views.suscribirse_no_pagadas.
        @route {POST} /contenido/<int:contenido_id_conte>/reportar/ - Permite a los usuarios reportar un contenido. Utiliza la vista views.reportar_contenido.
        @route {GET} /admin/reportes/ - Muestra los reportes de contenido en la administración. Utiliza la vista views.ver_reportes.
        @route {GET} /historial-compras/ - Muestra el historial de compras del usuario. Utiliza la vista views.historial_compras_view.
        @route {GET} /ventas/ - Lista las ventas realizadas. Utiliza la vista views.VentaListView.
        @route {GET} /contenido/registro/<int:pk>/ - Muestra el registro de un contenido. Utiliza la vista views.contenido_registro.
    '''