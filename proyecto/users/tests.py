from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Role
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Permission

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('role_based_redirect'))
        self.assertEqual(response.status_code, 302)  # Verifica la redirección

    def test_create_user_view(self):
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
        response = self.client.post(reverse('delete_user', args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 302)  # Verifica la redirección después de la eliminación
        self.assertFalse(User.objects.filter(id=self.admin_user.id).exists())  # Verifica que el usuario fue eliminado

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)  # Verifica que la página se carga correctamente
        self.assertContains(response, 'admin')  # Verifica que el usuario admin aparece en la lista
