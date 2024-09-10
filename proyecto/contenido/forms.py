from django import forms
from .models import Contenido
from django.utils import timezone

class ContenidoForm(forms.ModelForm):
    '''
    @class ContenidoForm
    @extends forms.ModelForm
    @description Formulario para el modelo 'Contenido'. Gestiona los campos y etiquetas del contenido, incluyendo un campo opcional para la imagen.
    '''
    class Meta:
        model = Contenido
        fields = ['titulo_conte', 'tipo_conte', 'texto_conte', 'estado_conte', 'fecha_conte', 'imagen_conte']
        labels = {
            'titulo_conte': 'Título del Contenido',
            'tipo_conte': 'Tipo de Contenido',
            'texto_conte': 'Texto del Contenido',
            'estado_conte': 'Estado del Contenido',
            'fecha_conte': 'Fecha del Contenido',
            'imagen_conte': 'Imagen del Contenido (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super(ContenidoForm, self).__init__(*args, **kwargs)
        self.fields['fecha_conte'].initial = timezone.now().date()  # Establecer la fecha actual
