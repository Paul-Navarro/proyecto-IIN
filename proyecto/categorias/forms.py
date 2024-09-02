from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 
                  'es_moderada', 
                  'es_pagada', 
                  'para_suscriptores',
                  'tipo_contenido',
                  'descripcion']
