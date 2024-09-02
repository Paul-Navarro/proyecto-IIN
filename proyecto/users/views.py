from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from contenido.models import Contenido



from django.shortcuts import render

def home(request):
    """
    @function home
    @description Renderiza la página de inicio mostrando todos los contenidos disponibles.
    """
    contenidos = Contenido.objects.all()
    return render(request, 'home/index.html', {'contenidos': contenidos})


@login_required
def role_based_redirect(request):
    """
    @function role_based_redirect
    @description Redirige al usuario a una página específica basada en su rol.
    
    Verifica el rol del usuario y redirige a la página correspondiente basada en el rol. 
    Si el rol no coincide con ninguno de los roles definidos, se redirige a la página de inicio.
    """
    user = request.user

    # Verificar si el correo está verificado
    
    if user.has_role('Admin'):
        return redirect('admin_dashboard')
    elif user.has_role('Editor'):
        return redirect('editor_dashboard')
    elif user.has_role('Publicador'):
        return redirect('publicador_dashboard')
    elif user.has_role('Suscriptor'):
        return redirect('suscriptor_dashboard')
    elif user.has_role('Autor'):
        return redirect('autor_dashboard')
    else:
        return redirect('home')  # Redirige a la página por defecto si no tiene un rol específico

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
    return render(request, '../templates/editor/dashboard.html')

@login_required
def publicador_dashboard(request):
    """
    @function publicador_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Publicador.
    """
    return render(request, '../templates/publicador/dashboard.html')

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
    return render(request, '../templates/autor/dashboard.html')


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

