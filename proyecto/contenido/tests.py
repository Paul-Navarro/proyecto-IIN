from django.test import TestCase
from django.urls import reverse
from .models import Contenido


# NO FUNCIONA AUN ESTE TEST, ESPERAR A QUE SE TERMINE DE MODIFICAR LA APP "contenido"
class ContenidoViewsTest(TestCase):
    '''
    @class ContenidoViewsTest
    @extends TestCase
    @description Pruebas para las vistas relacionadas con el modelo 'Contenido'. Incluye pruebas para listar, crear, actualizar y eliminar contenido. Algunas pruebas están desactivadas temporalmente mientras se modifican las vistas correspondientes.
    '''
    def setUp(self):
        # Crear algunos contenidos para probar
        Contenido.objects.create(
            titulo_conte="Contenido 1",
            tipo_conte="Tipo 1",
            texto_conte="Texto del contenido 1",
            estado_conte="Publicado",
            fecha_conte="2023-09-01"
        )
        Contenido.objects.create(
            titulo_conte="Contenido 2",
            tipo_conte="Tipo 2",
            texto_conte="Texto del contenido 2",
            estado_conte="Borrador",
            fecha_conte="2023-09-02"
        )

    def test_contenido_list_view(self):
        response = self.client.get(reverse('contenido_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'autor/contenido_list.html')
        self.assertContains(response, "Contenido 1")
        self.assertContains(response, "Contenido 2")

    # Se ha comentado la prueba para contenido_detail porque la vista está comentada
    """
    def test_contenido_detail_view(self):
        contenido = Contenido.objects.get(titulo_conte="Contenido 1")
        response = self.client.get(reverse('contenido_detail', args=[contenido.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'autor/contenido_detail.html')
        self.assertContains(response, "Texto del contenido 1")
    """

    def test_contenido_create_view(self):
        data = {
            'titulo_conte': 'Nuevo Contenido',
            'tipo_conte': 'Tipo 3',
            'texto_conte': 'Texto del nuevo contenido',
            'estado_conte': 'Publicado',
            'fecha_conte': '2023-09-03',
        }
        response = self.client.post(reverse('contenido_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(Contenido.objects.filter(titulo_conte='Nuevo Contenido').exists())

    def test_contenido_update_view(self):
        contenido = Contenido.objects.get(titulo_conte="Contenido 1")
        data = {
            'titulo_conte': 'Contenido 1 Actualizado',
            'tipo_conte': 'Tipo 1',
            'texto_conte': 'Texto actualizado del contenido 1',
            'estado_conte': 'Publicado',
            'fecha_conte': '2023-09-01',
        }
        response = self.client.post(reverse('contenido_update', args=[contenido.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        contenido.refresh_from_db()
        self.assertEqual(contenido.titulo_conte, 'Contenido 1 Actualizado')

    def test_contenido_delete_view(self):
        contenido = Contenido.objects.get(titulo_conte="Contenido 1")
        response = self.client.post(reverse('contenido_delete', args=[contenido.pk]))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertFalse(Contenido.objects.filter(pk=contenido.pk).exists())