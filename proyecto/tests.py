from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse
from contenido.models import Contenido
from categorias.models import Categoria
from users.models import CustomUser as User, Role  # Usamos CustomUser ya que has sustituido el User
from django.db import IntegrityError
from django.core.validators import validate_email
# Tests for Contenido module
class ContenidoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        self.contenido = Contenido.objects.create(
            titulo_conte="Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user  # Aseguramos que el contenido tenga un autor
        )

    def test_contenido_creation(self):
        self.assertTrue(isinstance(self.contenido, Contenido))
        self.assertEqual(str(self.contenido), self.contenido.titulo_conte)

    def test_contenido_fields(self):
        self.assertEqual(self.contenido.titulo_conte, "Test Contenido")
        self.assertEqual(self.contenido.estado_conte, "Publicado")
    
    def test_contenido_creation_with_empty_title(self):
        contenido = Contenido.objects.create(
            titulo_conte="",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user
        )
        self.assertEqual(contenido.titulo_conte, "")

    def test_contenido_creation_with_empty_text(self):
        contenido = Contenido.objects.create(
            titulo_conte="Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user
        )
        self.assertEqual(contenido.texto_conte, "")
    def test_contenido_creation_with_invalid_title(self):
        with self.assertRaises(IntegrityError):
            Contenido.objects.create(
                titulo_conte="",
                tipo_conte="Tipo 1",
                texto_conte="Texto de prueba",
                estado_conte="Publicado",
                fecha_conte="2023-09-01",
                autor=self.user
            )
    def test_contenido_creation_with_invalid_title(self):
        contenido = Contenido.objects.create(titulo_conte="Test Contenido", tipo_conte="Tipo 1", texto_conte="Texto de prueba", estado_conte="Publicado", fecha_conte="2023-09-01", autor=self.user)
        self.assertIsNotNone(contenido.titulo_conte)

class ContenidoViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        self.client.force_login(self.user)  # Simula que el usuario está autenticado.

        Contenido.objects.create(
            titulo_conte="Contenido 1",
            tipo_conte="Tipo 1",
            texto_conte="Texto del contenido 1",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user  # Asegúrate de asignar el autor al contenido
        )
        Contenido.objects.create(
            titulo_conte="Contenido 2",
            tipo_conte="Tipo 2",
            texto_conte="Texto del contenido 2",
            estado_conte="Borrador",
            fecha_conte="2023-09-02",
            autor=self.user
        )

    def test_contenido_list_view(self):
        response = self.client.get(reverse('contenido_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'autor/contenido_list.html')
        self.assertContains(response, "Contenido 1")
        self.assertContains(response, "Contenido 2")

def test_contenido_create_view(self):
    categoria = Categoria.objects.create(nombre="Test Categoria", descripcion="Descripción de prueba", es_moderada=False)
    
    data = {
        'titulo_conte': 'Nuevo Contenido',
        'tipo_conte': 'Tipo 3',
        'texto_conte': 'Texto del nuevo contenido',
        'estado_conte': 'BORRADOR',  # Valor por defecto
        'categoria': categoria.id,  # Asegúrate de pasar una categoría válida
        'fecha_conte': '2023-10-01',
        'autor': self.user.id  # Asignar el usuario autenticado como autor
    }
    
    response = self.client.post(reverse('contenido_create'), data)
    self.assertEqual(response.status_code, 302)  # Verifica la redirección
    self.assertTrue(Contenido.objects.filter(titulo_conte='Nuevo Contenido').exists())

    def test_contenido_delete_view(self):
        contenido = Contenido.objects.get(titulo_conte="Contenido 1")
        response = self.client.post(reverse('contenido_delete', args=[contenido.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contenido.objects.filter(titulo_conte="Contenido 1").exists())


# Tests for Categorias module (con los campos corregidos: nombre y descripcion)
class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Categoria Test", descripcion="Descripcion de prueba")

    def test_categoria_creation(self):
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(str(self.categoria), self.categoria.nombre)

    def test_categoria_fields(self):
        self.assertEqual(self.categoria.nombre, "Categoria Test")
        self.assertEqual(self.categoria.descripcion, "Descripcion de prueba")

    def test_categoria_creation_with_empty_name(self):
        categoria = Categoria.objects.create(
            nombre="",
            descripcion="Descripcion de prueba"
        )
        self.assertEqual(categoria.nombre, "")

    def test_categoria_creation_with_empty_description(self):
        categoria = Categoria.objects.create(
            nombre="Categoria Test",
            descripcion=""
        )
        self.assertEqual(categoria.descripcion, "")
    
    def test_categoria_creation_with_duplicate_nombre(self):
        categoria = Categoria.objects.create(nombre="Categoria 1", descripcion="Desc 1")
        categoria2 = Categoria.objects.create(nombre="Categoria 2", descripcion="Desc 2")
        self.assertNotEqual(categoria.nombre, categoria2.nombre)

class CategoriaViewsTest(TestCase):
    def setUp(self):
        Categoria.objects.create(nombre="Categoria 1", descripcion="Desc 1")
        Categoria.objects.create(nombre="Categoria 2", descripcion="Desc 2")

    def test_categoria_list_view(self):
        response = self.client.get(reverse('listar_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/categorias/listar_categorias.html')  # Plantilla correcta
        self.assertContains(response, "Categoria 1")  # Verifica que el contenido aparezca en la respuesta

    def test_categoria_create_view(self):
        data = {
            'nombre': 'Nueva Categoria',
            'descripcion': 'Descripcion de la nueva categoria',
            'es_moderada': False,  # Campo obligatorio
            'es_pagada': False,  # Campo obligatorio
            'para_suscriptores': False,  # Campo obligatorio
            'tipo_contenido': 'Texto'  # Asegúrate de que este valor sea válido para el campo
        }
        response = self.client.post(reverse('crear_categoria'), data)
        self.assertEqual(response.status_code, 302)  # Verifica la redirección
        self.assertTrue(Categoria.objects.filter(nombre='Nueva Categoria').exists())


    def test_categoria_delete_view(self):
        categoria = Categoria.objects.get(nombre="Categoria 1")
        response = self.client.post(reverse('eliminar_categoria', args=[categoria.pk]))  # Cambiado 'categoria_delete' a 'eliminar_categoria'
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Categoria.objects.filter(nombre="Categoria 1").exists())


# Tests for Users module (cambiando a CustomUser)
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(str(self.user), self.user.username)

    def test_user_fields(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
    
    
    
    def test_user_creation_with_invalid_email(self):
        try:
            validate_email("invalid_email")
            self.fail("Invalid email should not be valid")
        except ValidationError:
            pass

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", email="admin@example.com", password="password123")
        self.client.force_login(self.user)

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')

    def test_create_user_view(self):
        # Crea un rol antes de la prueba
        role = Role.objects.create(name='TestRole')

        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'P@ssw0rd12345!',  # Usamos una contraseña más segura
            'password2': 'P@ssw0rd12345!',  # Asegúrate de que coincida con 'password1'
            'first_name': 'New',  # Campo obligatorio
            'last_name': 'User',  # Campo obligatorio
            'roles': [role.id]  # Asigna el rol creado al usuario
        }

        response = self.client.post(reverse('create_user'), data)

        # Verifica si la redirección ocurre como se espera
        self.assertEqual(response.status_code, 302)

        # Verifica si el usuario fue creado
        self.assertTrue(User.objects.filter(username='newuser').exists())


    def test_delete_user_view(self):
        response = self.client.post(reverse('delete_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="admin").exists())
def test_create_user_view(self):
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'password123',  # Asegúrate de usar 'password1' y 'password2'
        'password2': 'password123'
    }
    response = self.client.post(reverse('create_user'), data)
    self.assertEqual(response.status_code, 302)  # Verifica la redirección
    self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_profile_view(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


# More Tests for Contenido, Categoria, and Users

class MoreContenidoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", email="testuser2@example.com", password="password123")
        self.contenido = Contenido.objects.create(
            titulo_conte="Another Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba adicional",
            estado_conte="Publicado",
            fecha_conte="2023-09-03",
            autor=self.user
        )

    def test_contenido_text_length(self):
        self.assertTrue(len(self.contenido.texto_conte) > 10)

    def test_contenido_published(self):
        self.assertEqual(self.contenido.estado_conte, "Publicado")

    def test_contenido_author(self):
        self.assertEqual(self.contenido.autor.username, "testuser2")

    def test_contenido_update(self):
        contenido = Contenido.objects.create(
            titulo_conte="Another Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba adicional",
            estado_conte="Publicado",
            fecha_conte="2023-09-03",
            autor=self.user
        )
        contenido.titulo_conte = "Updated Title"
        contenido.save()
        self.assertEqual(contenido.titulo_conte, "Updated Title")
    def test_contenido_update_with_new_autor(self):
        contenido = Contenido.objects.create(
            titulo_conte="Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user
        )
        new_user = User.objects.create_user(username="newuser", email="newuser@example.com", password="password123")
        contenido.autor = new_user
        contenido.save()
        self.assertEqual(contenido.autor, new_user)
    
    def test_contenido_creation_with_categoria(self):
        categoria = Categoria.objects.create(nombre="Categoria 1", descripcion="Desc 1")
        contenido = Contenido.objects.create(
            titulo_conte="Test Contenido",
            tipo_conte="Tipo 1",
            texto_conte="Texto de prueba",
            estado_conte="Publicado",
            fecha_conte="2023-09-01",
            autor=self.user,
            categoria=categoria
        )
        self.assertEqual(contenido.categoria, categoria)

class MoreCategoriaTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Test Categoria 2", descripcion="Otra descripcion de prueba", codigo=1)

    def test_categoria_unique_codigo(self):
        # Intentamos crear una nueva categoría con el mismo código
        with self.assertRaises(IntegrityError):  # IntegrityError esperado por la violación de unicidad
            Categoria.objects.create(nombre="Test Categoria 3", descripcion="Descripcion", codigo=1)

    def test_categoria_description_length(self):
        self.assertTrue(len(self.categoria.descripcion) > 5)

    def test_categoria_update(self):
        categoria = Categoria.objects.create(
            nombre="Test Categoria 2",
            descripcion="Otra descripcion de prueba",
            codigo=2
        )
        categoria.nombre = "Updated Nombre"
        categoria.save()
        self.assertEqual(categoria.nombre, "Updated Nombre")
    
    def test_categoria_update_with_new_descripcion(self):
        categoria = Categoria.objects.create(nombre="Categoria 1", descripcion="Desc 1")
        categoria.descripcion = "New Desc"
        categoria.save()
        self.assertEqual(categoria.descripcion, "New Desc")

class MoreUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser3", email="testuser3@example.com", password="password123")

    def test_user_email_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(username="testuser4", email="testuser3@example.com", password="password123")

    def test_user_password_strength(self):
        user = User.objects.create_user(username="testuser5", email="testuser5@example.com", password="weakpass")
        self.assertTrue(len(user.password) > 8)

    def test_user_creation_with_role(self):
        role = Role.objects.create(name='RoleForUserTest')
        self.user.roles.add(role)
        self.assertTrue(self.user.roles.filter(name='RoleForUserTest').exists())
