from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm,UserChangeForm, UserProfileChangeForm
from django.contrib import messages
from contenido.models import Contenido, Categoria, Rating, Favorito
from django.db.models import Q  # Para realizar búsquedas complejas con OR
from contenido.cron import AutopublicarContenido
from django.contrib.auth import update_session_auth_hash  # Para mantener la sesión después de cambiar la contraseña
from django.contrib.auth.forms import PasswordChangeForm  # Para el formulario de cambio de contraseña
from django.urls import reverse


# En tu vista, al procesar los datos


from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib import messages

from django.contrib.auth import get_user_model
from datetime import datetime

from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date


from django.utils.dateparse import parse_date  # Import to handle date parsing

#para las notificaciones
from django.views.generic import ListView
from .models import Notificacion
from django.http import JsonResponse
from django.db.models import Avg


def home(request):
    '''
    @function home
    @description Muestra la página principal del sitio, permitiendo la búsqueda y filtrado de contenidos según varias opciones como categoría, autor, moderación, suscripción, y fechas. Además, ejecuta una tarea programada para autopublicar contenido y muestra notificaciones no leídas del usuario autenticado.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /
    @returns {HttpResponse} Renderiza la plantilla 'home/index.html' con los contenidos filtrados, categorías, autores, roles y notificaciones.
    '''
    # DISPARADOR DE CRON
    cronjob = AutopublicarContenido()
    cronjob.do()

    # Obtener todas las categorías y autores
    categorias = Categoria.objects.all()
    autores = User.objects.all()

    # Inicializamos el queryset de contenidos como vacío
    contenidos = Contenido.objects.none()

    # Si el usuario está autenticado, obtenemos las categorías a las que está suscrito
    if request.user.is_authenticated:
        suscripciones_usuario = request.user.suscripcion_set.all().values_list('categoria_id', flat=True)

        # Filtramos las categorías a las que el usuario está suscrito, y además añadimos las categorías públicas
        categorias_accesibles = Categoria.objects.filter(
            Q(es_pagada=False, para_suscriptores=False) |  # Categorías públicas
            Q(id__in=suscripciones_usuario)  # Categorías a las que está suscrito
        )
    else:
        # Si el usuario no está autenticado, solo mostramos las categorías públicas
        categorias_accesibles = Categoria.objects.filter(es_pagada=False, para_suscriptores=False)

    # Filtrar los contenidos de las categorías accesibles
    contenidos = Contenido.objects.filter(categoria__in=categorias_accesibles, estado_conte='PUBLICADO', autopublicar_conte=True, vigencia_conte=False, es_destacado=False).order_by('-fecha_publicacion')

    contenidos_destacados = Contenido.objects.filter(
        categoria__in=categorias_accesibles,
        estado_conte='PUBLICADO',
        autopublicar_conte=True,
        vigencia_conte=False,
        es_destacado=True
    ).order_by('-fecha_publicacion')


# Verificar si se solicitó ver solo favoritos
    if request.GET.get('favoritos') == 'true' and request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user).values_list('contenido', flat=True)
        contenidos = contenidos.filter(id_conte__in=favoritos)

     # Calcular el promedio de calificaciones para cada contenido
    for contenido in contenidos:
        promedio_calificacion = Rating.objects.filter(contenido=contenido).aggregate(Avg('estrellas'))['estrellas__avg']
        contenido.promedio_calificacion = promedio_calificacion if promedio_calificacion else 0  # Asignar 0 si no tiene calificaciones

        # Verificar si el usuario está autenticado y si el contenido está en favoritos
        contenido.es_favorito = contenido.favoritos.filter(usuario=request.user).exists() if request.user.is_authenticated else False

    

    # Filtrar por categoría si está presente en la solicitud
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)

    # Verificar si se ha enviado un término de búsqueda
    query = request.GET.get('q')
    if query:
        contenidos = contenidos.filter(
            Q(titulo_conte__icontains=query) |  # Buscar por título
            Q(tags__nombre__icontains=query)    # Buscar por tags
        ).distinct()

    # Aplicar los filtros adicionales
    moderadas = 'moderadas' in request.GET
    no_moderadas = 'no_moderadas' in request.GET
    pagadas = 'pagadas' in request.GET
    suscriptores = 'suscriptores' in request.GET

    # Filtrar contenidos por moderación
    if moderadas and no_moderadas:
        contenidos = contenidos.filter(
            Q(categoria__es_moderada=True) | Q(categoria__es_moderada=False)
        )
    elif moderadas:
        contenidos = contenidos.filter(categoria__es_moderada=True)
    elif no_moderadas:
        contenidos = contenidos.filter(categoria__es_moderada=False)

    # Filtrar contenidos por pagadas
    if pagadas:
        contenidos = contenidos.filter(categoria__es_pagada=True)

    # Filtrar contenidos para suscriptores
    if suscriptores:
        contenidos = contenidos.filter(categoria__para_suscriptores=True)

    # Filtrar por rango de fechas
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if fecha_desde:
        contenidos = contenidos.filter(fecha_publicacion__gte=parse_date(fecha_desde))
    if fecha_hasta:
        contenidos = contenidos.filter(fecha_publicacion__lte=parse_date(fecha_hasta))

    # Filtrar por autor
    autor_id = request.GET.get('autor')
    if autor_id:
        contenidos = contenidos.filter(autor_id=autor_id)

    # Obtener el usuario y sus roles
    user = request.user
    roles_count = user.roles.count() if user.is_authenticated else 0

    # Obtener las notificaciones no leídas del usuario autenticado
    notificaciones_no_leidas = 0
    notificaciones = []
    if user.is_authenticated:
        notificaciones = Notificacion.objects.filter(usuario=user, leida=False)
        notificaciones_no_leidas = notificaciones.count()

    # Contexto para pasar a la plantilla
    context = {
        'contenidos': contenidos,
        'contenidos_destacados': contenidos_destacados,
        'categorias': categorias,
        'autores': autores,  # Pasamos los autores al contexto
        'has_admin_role': user.has_role('Admin') if user.is_authenticated else False,
        'has_autor_role': user.has_role('Autor') if user.is_authenticated else False,
        'has_editor_role': user.has_role('Editor') if user.is_authenticated else False,
        'has_publicador_role': user.has_role('Publicador') if user.is_authenticated else False,
        'has_financiero_role': user.has_role('Financiero') if user.is_authenticated else False,
        'has_multiple_roles': roles_count > 1,
        'has_single_role': roles_count == 1,
        'query': query,  # Pasar el término de búsqueda al contexto
        'notificaciones': notificaciones,  # Añadir las notificaciones al contexto
        'notificaciones_no_leidas': notificaciones_no_leidas,  # Añadir el conteo de no leídas
    }

    return render(request, 'home/index.html', context)



#para marcar notificaciones como leidas
def marcar_como_leida(request, id):
    '''
    @function marcar_como_leida
    @description Marca una notificación específica como leída para el usuario autenticado. Solo responde a solicitudes POST.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @param {int} id - El ID de la notificación que se va a marcar como leída.
    @route {POST} /notificaciones/marcar_como_leida/<int:id>/
    @returns {JsonResponse} Retorna una respuesta JSON con el estado 'ok' si la notificación se marca correctamente o un error si falla.
    '''
    # Verificar que el método sea POST y que el usuario esté autenticado
    if request.method == 'POST' and request.user.is_authenticated:
        # Obtener la notificación del usuario autenticado
        notificacion = get_object_or_404(Notificacion, id=id, usuario=request.user)
        
        # Marcar la notificación como leída
        notificacion.leida = True
        notificacion.save()
        
        # Devolver una respuesta JSON con estado 'ok'
        return JsonResponse({'status': 'ok'})
    
    # Si falla, devolver una respuesta de error
    return JsonResponse({'status': 'error'}, status=400)








@login_required
def role_based_redirect(request):
    '''
    @function role_based_redirect
    @description Redirige al usuario a un panel específico según su rol. Si el usuario tiene un solo rol, redirige automáticamente. Si tiene múltiples roles, ofrece una página para que seleccione el rol deseado. Si no tiene roles, asigna un rol predeterminado o maneja la situación de otra forma.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /role_based_redirect/
    @returns {HttpResponse|HttpRedirect} Redirige al panel correspondiente basado en el rol del usuario o muestra una página para seleccionar un rol si tiene múltiples.
    '''
    user = request.user
    roles = user.roles.all()  # Obtiene todos los roles del usuario
    
    if roles.count() == 0:
        # Asigna un rol predeterminado o redirige a una página por defecto
        # Aquí puedes asignar un rol por defecto o manejar de otra manera
        default_role_name = 'Suscriptor'  # Definir el rol predeterminado si es necesario
        return redirect_based_on_role(default_role_name)
    
    if roles.count() == 1 or roles.count() == 0:
        # Si solo tiene un rol, redirige automáticamente
        return redirect_based_on_role(roles.first().name)
    
    elif roles.count() > 1:
        # Si tiene múltiples roles, redirige a una página para que elija
        return render(request, '../templates/others/select_role.html', {'roles': roles})
    
    return redirect('home')  # Redirige a una página por defecto si no tiene roles


def redirect_based_on_role(role_name):
    '''
    @function redirect_based_on_role
    @description Redirige al usuario a la página correspondiente según su rol. Dependiendo del rol que se le pase, el usuario será redirigido a su panel específico.
    @param {str} role_name - El nombre del rol del usuario.
    @returns {HttpResponseRedirect} Redirige al panel de control correspondiente o a la página principal si no se reconoce el rol.
    '''
    if role_name == 'Admin':
        return redirect('admin_dashboard')
    elif role_name == 'Editor':
        return redirect('editor_dashboard')
    elif role_name == 'Publicador':
        return redirect('publicador_dashboard')
    elif role_name == 'Autor':
        return redirect('autor_dashboard')
    elif role_name == 'Suscriptor':
        return redirect('home') # Al ser un suscriptor se lo redirige a la pagina home
    elif role_name == 'Financiero':
        return redirect('venta_list')  # Redirigir a la página de ventas


    return redirect('home')

@login_required
def role_based_redirect_choice(request, role_name):
    '''
    @function role_based_redirect_choice
    @description Redirige al usuario al panel correspondiente según el rol que haya seleccionado. Usa la función `redirect_based_on_role` para gestionar la redirección.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @param {str} role_name - El nombre del rol seleccionado por el usuario.
    @returns {HttpResponseRedirect} Redirige al panel correspondiente según el rol seleccionado.
    '''
    return redirect_based_on_role(role_name)

@login_required
def admin_dashboard(request):
    '''
    @function admin_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Admin.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /admin/dashboard/
    @returns {HttpResponse} Renderiza la plantilla 'admin/users/dashboard.html'.
    '''
    return render(request, '../templates/admin/users/dashboard.html')

@login_required
def editor_dashboard(request):
    '''
    @function editor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Editor, mostrando una lista de todos los contenidos disponibles.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /editor/dashboard/
    @returns {HttpResponse} Renderiza la plantilla 'editor/dashboard.html' con la lista de contenidos.
    '''
    
    contenidos = Contenido.objects.all() 
    return render(request, '../templates/editor/dashboard.html',{'contenidos': contenidos})

@login_required
def publicador_dashboard(request):
    '''
    @function publicador_dashboard
    @description Ejecuta el cron job para autopublicar contenido y renderiza el panel de administración para usuarios con el rol de Publicador. Muestra una lista de contenidos disponibles y asigna el rol de usuario como 'Publicador'.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /publicador/dashboard/
    @returns {HttpResponse} Renderiza la plantilla 'publicador/dashboard.html' con la lista de contenidos y el rol de usuario.
    '''
    
    #DISPARADOR DE CRON
    cronjob = AutopublicarContenido()
    cronjob.do()
    
    contenidos = Contenido.objects.all()  
    user_role = 'Publicador'
    
    return render(request, '../templates/publicador/dashboard.html',{'contenidos': contenidos,'user_role': user_role})

@login_required
def suscriptor_dashboard(request):
    '''
    @function suscriptor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Suscriptor.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /suscriptor/dashboard/
    @returns {HttpResponse} Renderiza la plantilla 'suscriptor/dashboard.html'.
    '''
    return render(request, '../templates/suscriptor/dashboard.html')

@login_required
def autor_dashboard(request):
    '''
    @function autor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Autor, mostrando los contenidos creados por el autor actual.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /autor/dashboard/
    @returns {HttpResponse} Renderiza la plantilla 'autor/dashboard.html' con los contenidos del autor.
    '''
    
    contenidos = Contenido.objects.filter(autor=request.user)
    return render(request, '../templates/autor/dashboard.html',{'contenidos': contenidos})


User = get_user_model()

@login_required
def create_user(request):
    '''
    @function create_user
    @description Maneja la creación de un nuevo usuario.
    
    Muestra un formulario para crear un nuevo usuario y lo guarda en la base de datos si el formulario es válido. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la creación.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET|POST} /admin/users/create/
    @returns {HttpResponse} Renderiza la plantilla 'admin/users/create_user.html' con el formulario para crear un usuario.
    '''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin/users/create_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    '''
    @function edit_user
    @description Maneja la edición de un usuario existente.
    
    Muestra un formulario para editar un usuario y guarda los cambios en la base de datos si el formulario es válido. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la actualización.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @param {int} user_id - El ID del usuario a editar.
    @route {GET|POST} /admin/users/edit/<user_id>/
    @returns {HttpResponse} Renderiza la plantilla 'admin/users/edit_user.html' con el formulario para editar un usuario.
    '''
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'admin/users/edit_user.html', {'form': form, 'user': user})

@login_required
def editar_perfil(request):
    '''
    @function editar_perfil
    @description Maneja la edición del perfil del usuario actual.
    
    Permite al usuario actualizar su información personal, como nombre y foto de perfil, así como cambiar su contraseña. 
    Muestra mensajes de éxito o error según el resultado de las operaciones.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET|POST} /account/editar-perfil/
    @returns {HttpResponse} Renderiza la plantilla 'account/configurar_perfil.html' con los formularios de edición.
    '''
    user = request.user

    # Initialize both forms with user instance data
    form = UserProfileChangeForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        # Handle profile image upload or personal information changes
        if 'first_name' in request.POST or 'profile_image' in request.FILES:
            form = UserProfileChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Información personal actualizada exitosamente.')
                return redirect('editar_perfil')
            else:
                messages.error(request, 'Hubo un error al actualizar la información personal.')

        # Handle password change
        elif 'old_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevents logout after password change
                messages.success(request, 'Contraseña cambiada exitosamente.')
                return redirect('editar_perfil')
            else:
                messages.error(request, 'Hubo un error al cambiar la contraseña. Por favor, revisa los campos.')

    # Render the template with both forms
    return render(request, 'account/configurar_perfil.html', {
        'form': form,
        'password_form': password_form,
    })





@login_required
def delete_user(request, user_id):
    '''
    @function delete_user
    @description Maneja la eliminación de un usuario existente.
    
    Muestra un formulario de confirmación para eliminar un usuario y lo elimina de la base de datos si la solicitud es POST. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la eliminación.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @param {int} user_id - El ID del usuario a eliminar.
    @route {POST} /admin/users/delete/<user_id>/
    @returns {HttpResponse} Renderiza la plantilla 'admin/users/delete_user.html' para la confirmación de eliminación.
    '''
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('user_list')
    return render(request, 'admin/users/delete_user.html', {'user': user})

@login_required
def user_list(request):
    '''
    @function user_list
    @description Renderiza una lista de todos los usuarios en el sistema.
    
    Obtiene todos los usuarios y los pasa al contexto para su renderización en la plantilla 'admin/users/user_list.html'.
    @param {HttpRequest} request - La solicitud HTTP recibida.
    @route {GET} /admin/users/
    @returns {HttpResponse} Renderiza la plantilla 'admin/users/user_list.html' con la lista de usuarios.
    '''
    users = User.objects.all()
    return render(request, 'admin/users/user_list.html', {'users': users})



