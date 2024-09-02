from django.shortcuts import render, get_object_or_404, redirect
from .models import Contenido
from .forms import ContenidoForm

def contenido_list(request):
    contenidos = Contenido.objects.all()
    return render(request, 'autor/contenido_list.html', {'contenidos': contenidos})


def contenido_detail(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'autor/contenido_detail.html', {'contenido': contenido})

def contenido_create(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contenido_list')
    else:
        form = ContenidoForm()
    return render(request, 'autor/contenido_form.html', {'form': form})

def contenido_update(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        form = ContenidoForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            return redirect('contenido_list')
    else:
        form = ContenidoForm(instance=contenido)
    return render(request, 'autor/contenido_form.html', {'form': form})

def contenido_delete(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect('contenido_list')
    return render(request, 'autor/contenido_confirm_delete.html', {'contenido': contenido})
