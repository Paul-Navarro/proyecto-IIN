from django.db import models
from categorias.models import Categoria  # Importa el modelo Categoria


class Contenido(models.Model):
    '''
    @class Contenido
    @extends models.Model
    @description Modelo que representa el contenido en la aplicación. Incluye atributos como título, tipo, texto, estado, fecha, cantidad de visualizaciones, cantidad de comentarios y una imagen opcional.
    '''
    
    ESTADOS = [
        ('EN_REVISION', 'En Revisión'),
        ('PUBLICADO', 'Publicado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    id_conte = models.AutoField(primary_key=True)
    titulo_conte = models.CharField(max_length=255)
    tipo_conte = models.CharField(max_length=50)
    texto_conte = models.TextField()
    estado_conte = models.CharField(max_length=50)
    fecha_conte = models.DateField()
    cant_visualiz_conte = models.IntegerField(default=0)
    cant_coment_conte = models.IntegerField(default=0)
    imagen_conte = models.ImageField(upload_to='imagenes_contenido/', null=True, blank=True)  # Campo para la imagen
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con Categoria SIN ELIMINAR CONTENIDOS 
    #Como pidio el profe
    

    def __str__(self):
        return self.titulo_conte
