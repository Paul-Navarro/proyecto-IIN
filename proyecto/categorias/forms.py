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
                  'descripcion']
        widgets = {
            'es_pagada': forms.CheckboxInput(attrs={'id': 'id_es_pagada'}),
            'para_suscriptores': forms.CheckboxInput(attrs={'id': 'id_para_suscriptores'}),
        }
