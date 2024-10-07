from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Role
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    '''
    @class CustomUserCreationForm
    @extends UserCreationForm
    @description Formulario personalizado para la creación de usuarios. Este formulario extiende el formulario de creación de usuarios estándar de Django para incluir campos adicionales específicos del modelo `CustomUser`. Además, permite asignar múltiples roles a un usuario utilizando un widget de selección múltiple.
    '''

    # Permite seleccionar múltiples roles utilizando checkboxes
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),  # Lista de todos los roles disponibles
        widget=forms.CheckboxSelectMultiple,  # Cambia a Checkbox para facilitar la selección múltiple
        required=False  # Define si el campo de roles es obligatorio
    )

    class Meta:
        '''
        @description Clase Meta para especificar el modelo y los campos que se incluirán en el formulario de creación de usuarios.
        '''
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'roles')  # Incluye los campos que deseas utilizar

    def clean_roles(self):
        """
        Validación para asegurar que se seleccione al menos un rol.
        """
        roles = self.cleaned_data.get('roles')
        if not roles:  # Si no se selecciona ningún rol, lanzamos un error
            raise forms.ValidationError("Debes seleccionar al menos un rol.")
        return roles


class CustomUserChangeForm(UserChangeForm):
    '''
    @class CustomUserChangeForm
    @extends UserChangeForm
    @description Formulario personalizado para la edición de usuarios. Este formulario extiende el formulario de cambio de usuario estándar de Django para incluir campos adicionales específicos del modelo `CustomUser`, como la asignación de múltiples roles utilizando un widget de selección múltiple.
    '''

    # Permite seleccionar múltiples roles utilizando checkboxes
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),  # Lista de todos los roles disponibles
        widget=forms.CheckboxSelectMultiple,  # Cambia a Checkbox para facilitar la selección múltiple
        required=False  # Define si el campo de roles es obligatorio
    )

    class Meta:
        '''
        @description Clase Meta para especificar el modelo y los campos que se incluirán en el formulario de edición de usuarios.
        '''
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'roles', 'is_active', 'is_staff')  # Incluye los campos que deseas modificar

    def clean_roles(self):
        """
        Validación para asegurar que se seleccione al menos un rol.
        """
        roles = self.cleaned_data.get('roles')
        if not roles:
            raise forms.ValidationError("Debes seleccionar al menos un rol.")
        return roles

class CustomSignupForm(SignupForm):
    '''
    @class CustomSignupForm
    @extends SignupForm
    @description Formulario de registro personalizado que extiende el formulario de registro de `allauth`. Incluye los campos de nombre y apellido, además de los campos estándar de registro.
    '''
    first_name = forms.CharField(
        max_length=30, 
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})  # Adding placeholder here
    )
    
    last_name = forms.CharField(
        max_length=30, 
        label='Apellido',
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'})  # Adding placeholder here
    )    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    

User = get_user_model()
class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile_image']  # Incluye el campo de imagen