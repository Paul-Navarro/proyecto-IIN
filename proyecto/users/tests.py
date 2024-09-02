from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Role
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Permission

User = get_user_model()

class UserViewsTest(TestCase):
    """
    @class UserViewsTest
    @extends TestCase
    @description Clase de pruebas para las vistas relacionadas con el modelo CustomUser. Contiene métodos para probar la creación, edición, eliminación, y listado de usuarios, así como la redirección basada en roles.
    """
    def setUp(self):
        """
        @method setUp
        @description Configura el entorno necesario para realizar las pruebas. Crea roles y un usuario admin, asignando permisos y autenticando al usuario para pruebas que requieren inicio de sesión.
        """
        # Intentar obtener el rol de 'Admin', si no existe, crearlo
        self.admin_role, created = Role.objects.get_or_create(name='Admin')
        self.editor_role, created = Role.objects.get_or_create(name='Editor')
        
        # Agregar permisos al rol 'Admin'
        if created:
            permission = Permission.objects.get(codename='add_user')
            self.admin_role.permissions.add(permission)
        
        # Crear un usuario con rol de admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.admin_user.roles.add(self.admin_role)
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Autenticar el usuario admin para realizar pruebas que requieren login
        self.client.login(username='adminuser', password='leti1168')

    def test_role_based_redirect(self):
        """
        @method test_role_based_redirect
        @description Prueba para verificar que la vista de redirección basada en roles funciona correctamente. Se espera que la vista redirija al usuario a la página correspondiente según su rol.
        """
        response = self.client.get(reverse('role_based_redirect'))
        self.assertEqual(response.status_code, 302)  # Verifica la redirección

    def test_create_user_view(self):
        """
        @method test_create_user_view
        @description Prueba para verificar que la vista de creación de usuario funciona correctamente. Se envía una solicitud POST para crear un nuevo usuario y se verifica que la operación sea exitosa.
        """
        
        data = {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'password1': 'leti1168',
            'password2': 'leti1168',
            'roles': [self.editor_role.id],
        }
        response = self.client.post(reverse('create_user'), data)
        self.assertEqual(response.status_code, 302)  # Verifica la redirección después de la creación
        if response.status_code != 302:
            print(response.content.decode())  # Imprime el contenido de la respuesta para depuración
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Verifica que el usuario fue creado


    def test_edit_user_view(self):
        """
        @method test_edit_user_view
        @description Prueba para verificar que la vista de edición de usuario funciona correctamente. Se envía una solicitud POST para editar un usuario existente y se verifica que la operación sea exitosa.
        """
        data = {
            'username': 'admin',
            'email': 'admin_updated@example.com',
            'roles': [self.editor_role.id],
            'is_active': True,
            'is_staff': True
        }
        response = self.client.post(reverse('edit_user', args=[self.admin_user.id]), data)
        self.assertEqual(response.status_code, 302)  # Verifica la redirección después de la edición
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.email, 'admin_updated@example.com')  # Verifica que el email fue actualizado

    def test_delete_user_view(self):
        """
        @method test_delete_user_view
        @description Prueba para verificar que la vista de eliminación de usuario funciona correctamente. Se envía una solicitud POST para eliminar un usuario existente y se verifica que la operación sea exitosa.
        """
        response = self.client.post(reverse('delete_user', args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 302)  # Verifica la redirección después de la eliminación
        self.assertFalse(User.objects.filter(id=self.admin_user.id).exists())  # Verifica que el usuario fue eliminado

    def test_user_list_view(self):
        """
        @method test_user_list_view
        @description Prueba para verificar que la vista de listado de usuarios funciona correctamente. Se envía una solicitud GET para obtener la lista de usuarios y se verifica que la operación sea exitosa.
        """
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)  # Verifica que la página se carga correctamente
        self.assertContains(response, 'admin')  # Verifica que el usuario admin aparece en la lista
