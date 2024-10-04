from django.db import models
from categorias.models import Categoria  # Importa el modelo Categoria
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone


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
        ('BORRADOR', 'Borrador'),
        ('EDITADO', 'EDITADO'),
        ('A_PUBLICAR', 'A Publicar'),
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
    likes = models.IntegerField(default=0)
    unlikes = models.IntegerField(default=0)

    # Relación con el autor del contenido
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,  # Si el autor es eliminado, se establece en NULL
        null=True, 
        blank=True
    )
    fecha_publicacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo_conte
    
        # Método para verificar si el contenido debe ser publicado
    def autopublicar(self):
        if self.fecha_publicacion and self.fecha_publicacion <= timezone.now() and self.estado_conte == 'A_PUBLICAR':
            self.estado_conte = 'PUBLICADO'
            self.save()
    


class Rechazo(models.Model):
    '''
    @class Rechazo
    @extends models.Model
    @description Modelo que representa el rechazo de un contenido, incluyendo la razón y la fecha.
    '''
    
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='rechazos')
    razon = models.TextField()  # La razón del rechazo
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del rechazo

    def __str__(self):
        return f"Rechazo de {self.contenido.titulo_conte} en {self.fecha.strftime('%Y-%m-%d')}"
    
    
    
class VotoContenido(models.Model):
    VOTOS = [
        ('LIKE', 'Like'),
        ('UNLIKE', 'Unlike')
        
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    tipo_voto = models.CharField(max_length=6, choices=VOTOS, blank=True, null=True)
    fecha_voto = models.DateTimeField(auto_now_add=True)
    estrellas = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('usuario', 'contenido')  # Evita duplicados de votos


############# suscripciones #################
class Suscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.categoria.nombre}"
    
    class Meta:
        unique_together = ('usuario', 'categoria')  # Evita duplicados de suscripciones



