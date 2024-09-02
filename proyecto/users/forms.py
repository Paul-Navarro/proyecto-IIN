from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    @class CustomUserCreationForm
    @extends UserCreationForm
    @description Formulario personalizado para la creación de usuarios. Este formulario extiende el formulario de creación de usuarios estándar de Django para incluir campos adicionales específicos del modelo `CustomUser`.

    """
    class Meta:
        """
        @description Clase Meta para especificar el modelo y los campos que se incluirán en el formulario de creación de usuarios.

        """
        model = CustomUser
        fields = ('username', 'email', 'roles')  # Incluye los campos que deseas utilizar

class CustomUserChangeForm(UserChangeForm):
    """
    @class CustomUserCreationForm
    @extends UserCreationForm
    @description Formulario personalizado para la creación de usuarios. Este formulario extiende el formulario de creación de usuarios estándar de Django para incluir campos adicionales específicos del modelo `CustomUser`.

    Formulario personalizado para la edición de usuarios.    
    Este formulario extiende el formulario de cambio de usuario estándar de Django
    para incluir campos adicionales específicos del modelo CustomUser.
    """
    class Meta:
        ''' 
        @description Clase Meta para especificar el modelo y los campos que se incluirán en el formulario de creación de usuarios.
        '''
        model = CustomUser
        fields = ('username', 'email', 'roles', 'is_active', 'is_staff')  # Incluye los campos que deseas modificar
