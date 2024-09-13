from django.db import models
from categorias.models import Categoria  # Importa el modelo Categoria
from ckeditor.fields import RichTextField
from django.conf import settings


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
    
class Contenido(models.Model):
    '''
    @class Contenido
    @extends models.Model
    @description Modelo que representa el contenido en la aplicación.
    '''
    
    ESTADOS = [
        ('EN_REVISION', 'En Revisión'),
        ('PUBLICADO', 'Publicado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    id_conte = models.AutoField(primary_key=True)
    titulo_conte = models.CharField(max_length=255)
    tipo_conte = models.CharField(max_length=50)
    texto_conte = RichTextField()  # Cambiado de TextField a RichTextField
    estado_conte = models.CharField(max_length=50)
    fecha_conte = models.DateField()
    cant_visualiz_conte = models.IntegerField(default=0)
    cant_coment_conte = models.IntegerField(default=0)
    imagen_conte = models.ImageField(upload_to='imagenes_contenido/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # Relación con el autor del contenido
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,  # Si el autor es eliminado, se establece en NULL
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.titulo_conte
    
