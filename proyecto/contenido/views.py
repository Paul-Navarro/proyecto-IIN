from django.shortcuts import render, get_object_or_404, redirect
from .models import Contenido
from .forms import ContenidoForm
from categorias.models import Categoria

def contenido_list(request):
    '''
    @function contenido_list
    @description Muestra una lista de todos los contenidos.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @returns {HttpResponse} Respuesta renderizada con la lista de contenidos.
    '''
    contenidos = Contenido.objects.all()
    return render(request, 'autor/contenido_list.html', {'contenidos': contenidos})


def contenido_detail(request, pk):
    '''
    @function contenido_detail
    @description Muestra los detalles de un contenido específico.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a mostrar.
    @returns {HttpResponse} Respuesta renderizada con los detalles del contenido.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'autor/contenido_detail.html', {'contenido': contenido})

def contenido_create(request):
    '''
    @function contenido_create
    @description Crea un nuevo contenido. Maneja la validación del formulario y guarda el nuevo contenido.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @returns {HttpResponse} Redirige a la lista de contenidos después de crear uno nuevo o muestra el formulario con errores.
    '''
    # Obtener las categorías agrupadas
    categorias_no_moderadas = Categoria.objects.filter(es_moderada=False)
    categorias_moderadas = Categoria.objects.filter(es_moderada=True)
    categorias_pagadas = Categoria.objects.filter(es_pagada=True)
    categorias_suscriptores = Categoria.objects.filter(para_suscriptores=True)

    # Primera categoría no moderada como predeterminada
    primera_categoria_no_moderada = categorias_no_moderadas.first()

    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)  # Se añade request.FILES para manejar archivos
        if form.is_valid():
            form.save()
            return redirect('contenido_list')
    else:
        form = ContenidoForm(initial={'categoria': primera_categoria_no_moderada})  # Inicializar con categoría no moderada

    return render(request, 'autor/contenido_form.html', {
        'form': form,
        'categorias_no_moderadas': categorias_no_moderadas,
        'categorias_moderadas': categorias_moderadas,
        'categorias_pagadas': categorias_pagadas,
        'categorias_suscriptores': categorias_suscriptores,
    })

def contenido_update(request, pk):
    '''
    @function contenido_update
    @description Actualiza un contenido existente. Maneja la validación del formulario y guarda los cambios.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a actualizar.
    @returns {HttpResponse} Redirige a la lista de contenidos después de la actualización o muestra el formulario con errores.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    
    # Obtener las categorías agrupadas
    categorias_no_moderadas = Categoria.objects.filter(es_moderada=False)
    categorias_moderadas = Categoria.objects.filter(es_moderada=True)
    categorias_pagadas = Categoria.objects.filter(es_pagada=True)
    categorias_suscriptores = Categoria.objects.filter(para_suscriptores=True)

    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES, instance=contenido)  # Se añade request.FILES
        if form.is_valid():
            form.save()
            return redirect('contenido_list')
    else:
        form = ContenidoForm(instance=contenido)

    return render(request, 'autor/contenido_update.html', {
        'form': form,
        'categorias_no_moderadas': categorias_no_moderadas,
        'categorias_moderadas': categorias_moderadas,
        'categorias_pagadas': categorias_pagadas,
        'categorias_suscriptores': categorias_suscriptores,
    })

def contenido_delete(request, pk):
    '''
    @function contenido_delete
    @description Elimina un contenido existente después de confirmar la eliminación.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a eliminar.
    @returns {HttpResponse} Redirige a la lista de contenidos después de la eliminación o muestra una página de confirmación.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect('contenido_list')
    return render(request, 'autor/contenido_delete.html', {'contenido': contenido})
