from django.test import TestCase
from django.urls import reverse
from .models import Categoria


class CategoriaViewsTest(TestCase):
    def setUp(self):
        # Crear algunas categorías para probar
        Categoria.objects.create(nombre="Categoría 1")
        Categoria.objects.create(nombre="Categoría 2")

    def test_listar_categorias_view(self):
        response = self.client.get(reverse('listar_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/categorias/listar_categorias.html')
        self.assertContains(response, "Categoría 1")
        self.assertContains(response, "Categoría 2")

    def test_crear_categoria_view(self):
        data = {
            'nombre': 'Nueva Categoría',
            'es_moderada': True,
            'es_pagada': False,
            'para_suscriptores': True,
            'tipo_contenido': 'Artículo',
            'descripcion': 'Descripción de la nueva categoría',
        }
        response = self.client.post(reverse('crear_categoria'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        if response.status_code != 302:
            print(response.content.decode())  # Imprimir el contenido de la respuesta para depuración

    def test_editar_categoria_view(self):
        categoria = Categoria.objects.create(
            nombre="Categoría a Editar",
            es_moderada=False,
            es_pagada=True,
            para_suscriptores=False,
            tipo_contenido='Video',
            descripcion='Descripción original'
        )
        data = {
            'nombre': 'Categoría Editada',
            'es_moderada': True,
            'es_pagada': False,
            'para_suscriptores': True,
            'tipo_contenido': 'Artículo',
            'descripcion': 'Descripción editada',
        }
        response = self.client.post(reverse('editar_categoria', args=[categoria.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        if response.status_code != 302:
            print(response.content.decode())  # Imprimir el contenido de la respuesta para depuración
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, 'Categoría Editada')


    def test_eliminar_categoria_view(self):
        # Crear la categoría antes de intentar eliminarla
        categoria = Categoria.objects.create(nombre="Categoría a Eliminar")
        response = self.client.post(reverse('eliminar_categoria', args=[categoria.pk]))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertFalse(Categoria.objects.filter(pk=categoria.pk).exists())