from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'admin/categorias/listar_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'admin/categorias/crear_categoria.html', {'form': form})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'admin/categorias/editar_categoria.html', {'form': form})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'admin/categorias/eliminar_categoria.html', {'categoria': categoria})
