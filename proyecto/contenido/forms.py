from django import forms
from .models import Contenido
from categorias.models import Categoria
from django.utils import timezone
from django.forms.widgets import DateTimeInput

class ContenidoForm(forms.ModelForm):
    '''
    @class ContenidoForm
    @extends forms.ModelForm
    @description Formulario para el modelo 'Contenido'. Gestiona los campos y etiquetas del contenido, incluyendo un campo opcional para la imagen y la categoría.
    '''

    # Crear un campo de categoría
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),  # Mostrar todas las categorías por defecto
        required=True,
        label='Categoría'
    )

    # Campo para eliminar la imagen actual
    clear_image = forms.BooleanField(
        required=False,
        label="Eliminar la imagen actual",
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Contenido
        fields = ['titulo_conte', 'tipo_conte', 'texto_conte', 'fecha_conte', 'imagen_conte', 'categoria', 'tags','fecha_publicacion']
        labels = {
            'titulo_conte': 'Título del Contenido',
            'tipo_conte': 'Tipo de Contenido',
            'texto_conte': 'Texto del Contenido',
            'fecha_conte': 'Fecha del Contenido',
            'imagen_conte': 'Imagen de Portada (opcional)',
            'categoria': 'Categoría',
            'tags': 'Tags',
        }
        
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  # Mostrar los tags como checkboxes
            'fecha_publicacion': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContenidoForm, self).__init__(*args, **kwargs)

        # Obtener la primera categoría no moderada para asignarla como valor por defecto
        primera_categoria_no_moderada = Categoria.objects.filter(es_moderada=False).first()

        if primera_categoria_no_moderada:
            self.fields['categoria'].initial = primera_categoria_no_moderada

        # Personalizar el queryset del campo categoría
        self.fields['categoria'].queryset = Categoria.objects.all()

        # Establecer la fecha actual como fecha por defecto para el contenido, y hacer el campo readonly
        self.fields['fecha_conte'].initial = timezone.now().date()
        self.fields['fecha_conte'].widget.attrs['readonly'] = True  # Campo de solo lectura


