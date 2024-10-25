from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    @class CategoriaForm
    @extends forms.ModelForm
    @description Formulario para la creación y edición de objetos de la clase Categoria.
    Utiliza el modelo Categoria y define los campos que se mostrarán en el formulario. Estos campos permiten ingresar y modificar información relacionada con una categoría.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 
                  'es_moderada', 
                  'es_pagada', 
                  'para_suscriptores',
                  'tipo_contenido',
                  'descripcion',
                  'precio']
        widgets = {
            'es_pagada': forms.CheckboxInput(attrs={'id': 'id_es_pagada'}),
            'para_suscriptores': forms.CheckboxInput(attrs={'id': 'id_para_suscriptores'}),
            'precio': forms.NumberInput(attrs={'id': 'id_precio', 'step': '1','placeholder': 'Ingresa el precio'})
            
        }
        #verificacion para el precio
        def clean(self):
            """
            @function clean
            @description Realiza la validación de los campos del formulario. Si el campo es_pagada es verdadero,
            se asegura de que el campo precio esté completado. Si no se cumple esta condición, se añade un error al campo.
            @returns {dict} cleaned_data - Datos limpios y validados del formulario.
            """
            cleaned_data = super().clean()
            es_pagada = cleaned_data.get('es_pagada')
            precio = cleaned_data.get('precio')

            # Si es_pagada es True, el campo precio es obligatorio
            if es_pagada and not precio:
                self.add_error('precio', 'Debes especificar un precio para las categorías pagadas.')

            return cleaned_data
