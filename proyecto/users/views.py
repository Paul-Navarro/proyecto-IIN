from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages


@login_required
def role_based_redirect(request):
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
    else:
        return redirect('home')  # Redirige a la página por defecto si no tiene un rol específico

@login_required
def admin_dashboard(request):
    return render(request, '../templates/admin/dashboard.html')

@login_required
def editor_dashboard(request):
    
    return render(request, '../templates/editor/dashboard.html')

@login_required
def publicador_dashboard(request):
    return render(request, '../templates/publicador/dashboard.html')

@login_required
def suscriptor_dashboard(request):
    return render(request, '../templates/suscriptor/dashboard.html')


User = get_user_model()

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin/create_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('user_list')
    return render(request, 'admin/delete_user.html', {'user': user})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

