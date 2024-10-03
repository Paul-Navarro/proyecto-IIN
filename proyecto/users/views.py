from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm,UserChangeForm, UserProfileChangeForm
from django.contrib import messages
from contenido.models import Contenido, Categoria
from django.db.models import Q  # Para realizar búsquedas complejas con OR
from contenido.cron import AutopublicarContenido
from django.contrib.auth import update_session_auth_hash  # Para mantener la sesión después de cambiar la contraseña
from django.contrib.auth.forms import PasswordChangeForm  # Para el formulario de cambio de contraseña


from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib import messages


def home(request):
    
    #DISPARADOR DE CRON
    cronjob = AutopublicarContenido()
    cronjob.do()
    
    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    # Filtrar los contenidos publicados
    contenidos = Contenido.objects.filter(estado_conte='PUBLICADO')

    # Filtrar por autor si se ha enviado un autor en la URL
    autores_seleccionados = request.GET.getlist('autor')

    # Si hay autores seleccionados, filtrar por esos autores
    if autores_seleccionados:
        contenidos = contenidos.filter(autor_id__in=autores_seleccionados)

    # Verificar si se ha enviado el parámetro de la categoría en el GET
    categoria_id = request.GET.get('categoria')

    # Si el parámetro está presente, filtrar los contenidos por esa categoría
    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)

    # Verificar si se ha enviado el término de búsqueda
    query = request.GET.get('q')
    if query:
        # Filtrar los contenidos por título o por tags
         contenidos = contenidos.filter(
            Q(titulo_conte__icontains=query) |  # Buscar por título
            Q(tags__nombre__icontains=query) |  # Buscar por tags
            Q(autor__first_name__icontains=query) |  # Buscar por nombre del autor
            Q(autor__last_name__icontains=query)  # Buscar por apellido del autor
        ).distinct()  # Evitar duplicados si coinciden con ambos
    
     # Filtro de rango de fechas
    if request.GET.get('filtrar_fecha'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            contenidos = contenidos.filter(fecha_publicacion__range=[start_date, end_date])


    # Verificamos si los filtros adicionales están aplicados
    if 'moderadas' in request.GET:
        categorias = categorias.filter(es_moderada=True)
    if 'no_moderadas' in request.GET:
        categorias = categorias.filter(es_moderada=False)
    if 'pagadas' in request.GET:
        categorias = categorias.filter(es_pagada=True)
    if 'suscriptores' in request.GET:
        categorias = categorias.filter(para_suscriptores=True)

    if 'ordenar_fecha' in request.GET:
        contenidos = contenidos.order_by('-fecha_publicacion')

    # Obtener los autores para el formulario de filtro
    autores = User.objects.filter(contenido__estado_conte='PUBLICADO').distinct()


    # Obtener el usuario y sus roles
    user = request.user
    roles_count = user.roles.count() if user.is_authenticated else 0

    # Lógica de roles
    context = {
        'contenidos': contenidos,
        'categorias': categorias,
        'autores': autores,  # Pasar los autores al contexto para el filtro
        'autores_seleccionados': autores_seleccionados,  # Pasar los autores seleccionados al template
        'has_admin_role': user.has_role('Admin') if user.is_authenticated else False,
        'has_autor_role': user.has_role('Autor') if user.is_authenticated else False,
        'has_editor_role': user.has_role('Editor') if user.is_authenticated else False,
        'has_publicador_role': user.has_role('Publicador') if user.is_authenticated else False,
        'has_multiple_roles': roles_count > 1,
        'has_single_role': roles_count == 1,
        'query': query  # Pasar el término de búsqueda al contexto
    }

    return render(request, 'home/index.html', context)

@login_required
def role_based_redirect(request):
    """
    Si el usuario tiene un solo rol, redirige directamente al panel correspondiente.
    Si tiene múltiples roles, ofrece una página para seleccionar el rol.
    """
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
    """
    Redirige a la página correspondiente según el rol.
    """
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

    return redirect('home')

@login_required
def role_based_redirect_choice(request, role_name):
    """
    Redirige al panel correspondiente basado en el rol seleccionado.
    """
    return redirect_based_on_role(role_name)

@login_required
def admin_dashboard(request):
    """
    @function admin_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Admin.
    """
    return render(request, '../templates/admin/users/dashboard.html')

@login_required
def editor_dashboard(request):
    """
    @function editor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Editor.
    """
    
    contenidos = Contenido.objects.all() 
    return render(request, '../templates/editor/dashboard.html',{'contenidos': contenidos})

@login_required
def publicador_dashboard(request):
    
    #DISPARADOR DE CRON
    cronjob = AutopublicarContenido()
    cronjob.do()
    """
    @function publicador_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Publicador.
    """
    contenidos = Contenido.objects.all()  
    user_role = 'Publicador'
    
    return render(request, '../templates/publicador/dashboard.html',{'contenidos': contenidos,'user_role': user_role})

@login_required
def suscriptor_dashboard(request):
    """
    @function suscriptor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Suscriptor.
    """
    return render(request, '../templates/suscriptor/dashboard.html')

@login_required
def autor_dashboard(request):
    """
    @function autor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Autor.
    """
    
    contenidos = Contenido.objects.filter(autor=request.user)
    return render(request, '../templates/autor/dashboard.html',{'contenidos': contenidos})


User = get_user_model()

@login_required
def create_user(request):
    """
    @function create_user
    @description Maneja la creación de un nuevo usuario.
    
    Muestra un formulario para crear un nuevo usuario y lo guarda en la base de datos si el formulario es válido. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la creación.
    """
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
    """
    @function edit_user
    @description Maneja la edición de un usuario existente.
    
    Muestra un formulario para editar un usuario y guarda los cambios en la base de datos si el formulario es válido. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la actualización.
    """
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
    """
    @function delete_user
    @description Maneja la eliminación de un usuario existente.
    
    Muestra un formulario de confirmación para eliminar un usuario y lo elimina de la base de datos si la solicitud es POST. 
    Muestra un mensaje de éxito y redirige a la lista de usuarios tras la eliminación.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('user_list')
    return render(request, 'admin/users/delete_user.html', {'user': user})

@login_required
def user_list(request):
    """
    @function user_list
    @description Renderiza una lista de todos los usuarios en el sistema.
    
    Obtiene todos los usuarios y los pasa al contexto para su renderización en la plantilla 'admin/users/user_list.html'.
    """
    users = User.objects.all()
    return render(request, 'admin/users/user_list.html', {'users': users})

