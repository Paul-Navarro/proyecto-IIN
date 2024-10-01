from django.shortcuts import render, get_object_or_404, redirect
from .models import Contenido,Rechazo,VotoContenido
from .forms import ContenidoForm
from categorias.models import Categoria
from django.shortcuts import render, redirect
from .forms import ContenidoForm
from categorias.models import Categoria
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Suscripcion,Categoria
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def contenido_list(request):
    '''
    @function contenido_list
    @description Muestra una lista de todos los contenidos, con opción de búsqueda por título y tags.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @returns {HttpResponse} Respuesta renderizada con la lista de contenidos filtrados.
    '''
    
    user = request.user
    contenidos = Contenido.objects.filter(autor=user)  # Mostrar solo los contenidos del autor


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
    return render(request, 'home/contenido_detail.html', {'contenido': contenido})

def contenido_detail_editor(request, pk):
    '''
    @function contenido_detail
    @description Muestra los detalles de un contenido específico.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a mostrar.
    @returns {HttpResponse} Respuesta renderizada con los detalles del contenido.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'editor/contenido_detail_editor.html', {'contenido': contenido})

def contenido_detail_publicador(request, pk):
    '''
    @function contenido_detail
    @description Muestra los detalles de un contenido específico.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a mostrar.
    @returns {HttpResponse} Respuesta renderizada con los detalles del contenido.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'publicador/contenido_detail_publicador.html', {'contenido': contenido})

def contenido_detail_autor(request, pk):
    '''
    @function contenido_detail
    @description Muestra los detalles de un contenido específico.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a mostrar.
    @returns {HttpResponse} Respuesta renderizada con los detalles del contenido.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'autor/contenido_detail_autor.html', {'contenido': contenido})

def contenido_create(request):
    '''
    @function contenido_create
    @description Crea un nuevo contenido. Asigna el autor automáticamente y maneja la validación del formulario.
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
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            # No guardar el formulario inmediatamente
            contenido = form.save(commit=False)

            # Asignar el autor al usuario actual (el que está creando el contenido)
            contenido.autor = request.user

            # Verificar si la categoría seleccionada es no moderada
            if contenido.categoria and not contenido.categoria.es_moderada:
                contenido.estado_conte = 'PUBLICADO'
            else:
                contenido.estado_conte = 'BORRADOR'

            
            contenido.save()  # Guardar el contenido con el estado ajustado y el autor
            form.save_m2m()
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
            # Guardar el contenido pero no las relaciones many-to-many (como los tags)
            contenido = form.save(commit=False)

            # Si el campo clear_image está marcado, eliminar la imagen
            if form.cleaned_data.get('clear_image'):
                contenido.imagen_conte.delete()  # Eliminar la imagen del campo

            # Guardar el contenido con los campos actualizados
            contenido.save()

            # Guardar los tags (relaciones many-to-many)
            form.save_m2m()

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

def contenido_update_editor(request, pk):
    '''
    @function contenido_update
    @description Actualiza un contenido existente. Maneja la validación del formulario y guarda los cambios.
    @param {HttpRequest} request - El objeto de solicitud HTTP.
    @param {int} pk - El ID del contenido a actualizar.
    @returns {HttpResponse} Redirige a la lista de contenidos después de la actualización o muestra el formulario con errores.
    '''
    contenido = get_object_or_404(Contenido, pk=pk)
    rechazos = contenido.rechazos.all()  # Obtener todos los rechazos asociados a este contenido
    
    # Obtener las categorías agrupadas
    categorias_no_moderadas = Categoria.objects.filter(es_moderada=False)
    categorias_moderadas = Categoria.objects.filter(es_moderada=True)
    categorias_pagadas = Categoria.objects.filter(es_pagada=True)
    categorias_suscriptores = Categoria.objects.filter(para_suscriptores=True)

    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES, instance=contenido)  # Se añade request.FILES
        if form.is_valid():
            # Guardar el contenido pero no las relaciones many-to-many (como los tags)
            contenido = form.save(commit=False)

            # Si el campo clear_image está marcado, eliminar la imagen
            if form.cleaned_data.get('clear_image'):
                contenido.imagen_conte.delete()  # Eliminar la imagen del campo
                
            #La fecha de programacion de publicacion del contenido se mantiene intacta.    
            contenido.fecha_publicacion = Contenido.objects.get(pk=pk).fecha_publicacion
            contenido.estado_conte = 'EDITADO'  # Cambiar el estado a "EDITADO"

            # Guardar el contenido con los campos actualizados
            contenido.save()

            # Guardar los tags (relaciones many-to-many)
            form.save_m2m()

            return redirect('editor_dashboard')
    else:
        form = ContenidoForm(instance=contenido)

    return render(request, 'editor/contenido_update_editor.html', {
        'form': form,
        'categorias_no_moderadas': categorias_no_moderadas,
        'categorias_moderadas': categorias_moderadas,
        'categorias_pagadas': categorias_pagadas,
        'categorias_suscriptores': categorias_suscriptores,
        'rechazos': rechazos
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

def contenido_cambiar_estado(request, id_conte):
    # Obtener el contenido por su ID
    contenido = get_object_or_404(Contenido, id_conte=id_conte)

    if request.method == 'POST':
        # Obtener el nuevo estado desde el formulario
        nuevo_estado = request.POST.get('nuevo_estado')

        if nuevo_estado in ['PUBLICADO', 'RECHAZADO', 'EDITADO','BORRADOR','A_PUBLICAR']:
            # Actualizar el estado del contenido
            contenido.estado_conte = nuevo_estado
            contenido.save()
            messages.success(request, f"El estado del contenido '{contenido.titulo_conte}' se ha actualizado a '{nuevo_estado}'.")
        else:
            messages.error(request, "Estado no válido.")

    return redirect('gestionar_contenido')  # Redirigir a la lista de contenidos

def gestionar_contenido(request):
    """
    @function gestionar_contenido
    @description Redirige a la página de gestión de contenidos para el publicador.
    @param {HttpRequest} request - La solicitud HTTP.
    @returns {HttpResponse} Renderiza la plantilla 'publicador/contenido_gestion.html'.
    """
    contenidos = Contenido.objects.all()
    return render(request, 'publicador/contenido_gestion.html', {'contenidos': contenidos})


@csrf_exempt
def contenido_cambiar_estado_KANBAN(request, id_conte):
    # Obtener el contenido por su ID
    contenido = get_object_or_404(Contenido, pk=id_conte)

    if request.method == 'POST':
        try:
            # Obtener el nuevo estado desde la solicitud AJAX
            data = json.loads(request.body)
            nuevo_estado = data.get('nuevo_estado')

            if nuevo_estado in ['PUBLICADO', 'RECHAZADO', 'EDITADO', 'BORRADOR', 'A_PUBLICAR']:
                
                if nuevo_estado == 'RECHAZADO':
                    razon_rechazo = data.get('razon_rechazo', '')
                    Rechazo.objects.create(contenido=contenido, razon=razon_rechazo)
                
                # Actualizar el estado del contenido
                old_state = contenido.estado_conte
                contenido.estado_conte = nuevo_estado
                
                contenido.save()
                
                return JsonResponse({
                'success': True,
                'old_state': old_state,
                'new_state': nuevo_estado,
                'titulo': contenido.titulo_conte,
                'fecha_publicacion': contenido.fecha_publicacion
 })
            else:
                return JsonResponse({'success': False, 'error': 'Estado no válido'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error al procesar los datos'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    

def editor_dashboard(request):
    """
    @function editor_dashboard
    @description Renderiza el panel de administración para usuarios con el rol de Editor.
    """
    
    contenidos = Contenido.objects.all() 
    return render(request, '../templates/editor/dashboard.html',{'contenidos': contenidos})

@csrf_exempt
@login_required
def like_contenido(request, id_conte):
    contenido = get_object_or_404(Contenido, id_conte=id_conte)
    usuario = request.user

    if request.method == 'POST':
        # Verificar si el usuario ya ha dado like o unlike
        voto, created = VotoContenido.objects.get_or_create(usuario=usuario, contenido=contenido)

        if not created and voto.tipo_voto == 'LIKE':
            # Si el usuario ya ha dado like, lo quitamos
            contenido.likes -= 1
            voto.delete()  # Eliminamos el voto
        else:
            if voto.tipo_voto == 'UNLIKE':
                # Si tenía un unlike, reducimos el contador de unlikes
                contenido.unlikes -= 1
            # Aumentamos el contador de likes
            voto.tipo_voto = 'LIKE'
            contenido.likes += 1
            voto.save()

        contenido.save()
        return JsonResponse({'likes': contenido.likes, 'unlikes': contenido.unlikes})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
def unlike_contenido(request, id_conte):
    contenido = get_object_or_404(Contenido, id_conte=id_conte)
    usuario = request.user

    if request.method == 'POST':
        # Verificar si el usuario ya ha dado unlike o like
        voto, created = VotoContenido.objects.get_or_create(usuario=usuario, contenido=contenido)

        if not created and voto.tipo_voto == 'UNLIKE':
            # Si ya ha dado unlike, lo quitamos
            contenido.unlikes -= 1
            voto.delete()  # Eliminamos el voto
        else:
            if voto.tipo_voto == 'LIKE':
                # Si tenía un like, reducimos el contador de likes
                contenido.likes -= 1
            # Aumentamos el contador de unlikes
            voto.tipo_voto = 'UNLIKE'
            contenido.unlikes += 1
            voto.save()

        contenido.save()
        return JsonResponse({'likes': contenido.likes, 'unlikes': contenido.unlikes})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


#--------------------------------------


######### vistas para suscripciones ################
def suscripciones_view(request):
    if request.user.is_authenticated:
        usuario = request.user

        # Obtener las categorías a las que el usuario ya está suscrito
        suscripciones = Suscripcion.objects.filter(usuario=usuario)
        categorias_suscritas = [s.categoria for s in suscripciones]

        # Solo mostrar las categorías que son pagadas y a las que el usuario NO está suscrito
        categorias_no_suscritas = Categoria.objects.filter(es_pagada=True).exclude(id__in=[cat.id for cat in categorias_suscritas])

        context = {
            'categorias_suscritas': categorias_suscritas,   # Para mostrar las suscripciones actuales, si es necesario
            'categorias_no_suscritas': categorias_no_suscritas,  # Solo categorías pagadas a las que no está suscrito
            'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
        }
        return render(request, 'suscripciones/inicio_suscripcion.html', context)

    return render(request, 'suscripciones/inicio_suscripcion.html')


#vista para contacto
def contact_us(request):
    return render(request, 'anhadidos/contact_us.html')
    
#vista para la pasarela de pago

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
def comprar_suscripcion(request):
    if request.method == 'POST' and request.user.is_authenticated:
        usuario = request.user
        categorias_seleccionadas = request.POST.getlist('categorias')  # Recibe las categorías seleccionadas por el usuario

        if not categorias_seleccionadas:
            return JsonResponse({'error': 'No seleccionaste ninguna categoría.'}, status=400)

        line_items = []
        precio_por_categoria = 1000  # Precio en centavos (10.00 USD por ejemplo)

        # Crear los line_items para Stripe basado en las categorías seleccionadas
        for categoria_id in categorias_seleccionadas:
            categoria = Categoria.objects.get(id=categoria_id)
            if categoria.es_pagada:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Suscripción a {categoria.nombre}',  # Nombre de la suscripción
                        },
                        'unit_amount': precio_por_categoria,  # Monto por suscripción
                    },
                    'quantity': 1,
                })

        # Crear una sesión de Stripe Checkout y pasar los IDs de categorías en los metadatos
        dominio = "http://localhost:8000"
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=dominio + '/contenido/success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=dominio + '/contenido/cancel/',
                metadata={
                    'categorias_ids': ','.join(categorias_seleccionadas)  # Pasar los IDs de las categorías seleccionadas
                }
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


#@login_required(login_url='account_login')
def suscripcion_exitosa(request):
    # Depurar el estado de request.user
    print(f"request.user: {request.user}")
    print(f"request.user.is_authenticated: {request.user.is_authenticated}")
    
    session_id = request.GET.get('session_id')
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)

        # Obtener el usuario actual
        usuario = request.user

        # Verifica si el usuario es anónimo antes de hacer algo
        if usuario.is_anonymous:
            print("Error: Usuario anónimo detectado")
            return redirect('account_login')

        # Obtener los IDs de las categorías desde los metadatos de la sesión
        categorias_ids = session.metadata['categorias_ids'].split(',')

        # Crear suscripciones para las categorías seleccionadas
        categorias_seleccionadas = Categoria.objects.filter(id__in=categorias_ids)
        for categoria in categorias_seleccionadas:
            Suscripcion.objects.get_or_create(usuario=usuario, categoria=categoria)

        return render(request, 'suscripciones/success.html')

    return redirect('suscripciones_view')


def suscripcion_cancelada(request):
    return render(request, 'suscripciones/cancel.html')

