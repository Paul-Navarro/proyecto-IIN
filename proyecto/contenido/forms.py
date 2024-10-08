from django import forms
from .models import Contenido, ReporteContenido
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

    class Meta:
        model = Contenido
        fields = ['titulo_conte', 'tipo_conte', 'texto_conte', 'fecha_conte', 'imagen_conte', 'categoria', 'tags','fecha_publicacion', 'fecha_vigencia']
        labels = {
            'titulo_conte': 'Título del contenido',
            'tipo_conte': 'Tipo de contenido',
            'texto_conte': 'Texto del contenido',
            'fecha_conte': 'Fecha creacion del contenido',
            'imagen_conte': 'Imagen de Portada (Obligatorio)',
            'categoria': 'Categoría',
            'tags': 'Tags',
        }
        
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  # Mostrar los tags como checkboxes
            'fecha_publicacion': DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_vigencia': DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(ContenidoForm, self).__init__(*args, **kwargs)

        # Obtener la primera categoría no moderada para asignarla como valor por defecto
        primera_categoria_no_moderada = Categoria.objects.filter(es_moderada=False).first()

        if primera_categoria_no_moderada:
            self.fields['categoria'].initial = primera_categoria_no_moderada
            
        if self.instance.pk:
            self.fields['fecha_publicacion'].required = False
            self.fields['fecha_vigencia'].required = False  # Edición: no es requerido
        else:
            self.fields['fecha_publicacion'].required = True   # Creación: es requerido
            self.fields['fecha_vigencia'].required = True   # Creación: es requerido

        # Personalizar el queryset del campo categoría
        self.fields['categoria'].queryset = Categoria.objects.all()

        # Establecer la fecha actual como fecha por defecto para el contenido, y hacer el campo readonly
        self.fields['fecha_conte'].initial = timezone.now().date()
        self.fields['fecha_conte'].widget.attrs['readonly'] = True  # Campo de solo lectura
         
        self.fields['imagen_conte'].required = True  # Aquí lo hacemos obligatorio a la imagen de portada

#formulario de contacto     
class ContactForm(forms.Form):
    '''
    @class ContactForm
    @extends forms.Form
    @description Formulario para que los usuarios puedan enviar un mensaje de contacto, incluyendo campos como nombre, correo electrónico, asunto y el mensaje en sí.
    '''
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre y apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    asunto = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje...'}))



#formulario para reporte de contenidos
class ReporteContenidoForm(forms.ModelForm):
    '''
    @class ReporteContenidoForm
    @extends forms.ModelForm
    @description Formulario utilizado para reportar un contenido específico. Permite a los usuarios enviar una razón o motivo por el cual están reportando el contenido.
    '''
    class Meta:
        model = ReporteContenido
        fields = ['razon']
        widgets = {
            'razon': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explica el motivo del reporte...'}),
        }
        labels = {
            'razon': 'Motivo del Reporte',
        }
