from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm

def listar_categorias(request):
    """
    @function listar_categorias
    @description Vista para listar todas las categorías existentes en el sistema.
    Esta vista recupera todas las instancias del modelo Categoria y las pasa al template 'listar_categorias.html'.
    @param request {HttpRequest} El objeto HttpRequest que contiene información sobre la solicitud actual.
    @return {HttpResponse} Renderiza el template con las categorías listadas.
    """
    categorias = Categoria.objects.all()
    return render(request, 'admin/categorias/listar_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    """
    @function crear_categoria
    @description Vista para la creación de una nueva categoría. Gestiona la creación de categorías a través de un formulario.
    Si se envía una solicitud POST con datos válidos, se guarda la nueva categoría y redirige a la vista de listado.
    @param request {HttpRequest} El objeto HttpRequest que contiene información sobre la solicitud actual.
    @return {HttpResponse} Renderiza el template con el formulario para crear una nueva categoría.
    """
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'admin/categorias/crear_categoria.html', {'form': form})

def editar_categoria(request, pk):
    """
    @function editar_categoria
    @description Vista para editar una categoría existente. Permite actualizar una categoría existente utilizando un formulario.
    Si la solicitud es POST y el formulario es válido, guarda los cambios y redirige a la vista de listado.
    @param request {HttpRequest} El objeto HttpRequest que contiene información sobre la solicitud actual.
    @param pk {int} El ID de la categoría que se desea editar.
    @return {HttpResponse} Renderiza el template con el formulario para editar la categoría seleccionada.
    """
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
    """
    @function eliminar_categoria
    @description Vista para eliminar una categoría existente. Solicita confirmación antes de eliminar una categoría del sistema.
    Si la solicitud es POST, elimina la categoría seleccionada y redirige a la vista de listado.
    @param request {HttpRequest} El objeto HttpRequest que contiene información sobre la solicitud actual.
    @param pk {int} El ID de la categoría que se desea eliminar.
    @return {HttpResponse} Renderiza el template para confirmar la eliminación de la categoría.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'admin/categorias/eliminar_categoria.html', {'categoria': categoria})
