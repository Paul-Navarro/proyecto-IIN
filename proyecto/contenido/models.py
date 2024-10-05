from django.db import models
from categorias.models import Categoria  # Importa el modelo Categoria
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone
from .models import Categoria


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
    autopublicar_conte = models.BooleanField(default=False)

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
        if self.fecha_publicacion and self.fecha_publicacion <= timezone.now() and self.estado_conte == 'PUBLICADO':
            self.autopublicar_conte = True
            self.save()
            
    def save(self, *args, **kwargs):
        # Detectar si el contenido ya existía en la base de datos
        if self.pk:
            # Obtener el contenido original desde la base de datos
            original = Contenido.objects.get(pk=self.pk)

            # Comparar si hubo cambios significativos en los campos
            if original.texto_conte != self.texto_conte or original.titulo_conte != self.titulo_conte:
                # Incrementar el número de versión basado en las versiones existentes
                version_num = self.versiones.count() + 1
                # Crear una nueva versión del contenido
                VersionContenido.objects.create(
                    contenido_original=self,
                    version_num=version_num,
                    titulo_conte=original.titulo_conte,
                    tipo_conte=original.tipo_conte,
                    texto_conte=original.texto_conte,
                    fecha_version=timezone.now(),
                )
        
        super(Contenido, self).save(*args, **kwargs)  # Guardar el contenido normalmente
    
class VersionContenido(models.Model):
    contenido_original = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='versiones')
    version_num = models.PositiveIntegerField()  # Número de versión
    titulo_conte = models.CharField(max_length=255)
    tipo_conte = models.CharField(max_length=50)
    texto_conte = RichTextField()  # El contenido en sí
    fecha_version = models.DateTimeField(default=timezone.now)  # Fecha de la versión
    
    def __str__(self):
        return f"{self.contenido_original.titulo_conte} - v{self.version_num}"

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
    
    
class CambioBorrador(models.Model):
    '''
    @class CambioBorrador
    @extends models.Model
    @description Modelo que representa el cambio de un contenido a la columna Borrador, incluyendo la razón y la fecha.
    '''
    
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='cambios_borrador')
    razon = models.TextField()  # La razón del cambio a Borrador
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del cambio

    def __str__(self):
        return f"Cambio a Borrador de {self.contenido.titulo_conte} el {self.fecha.strftime('%Y-%m-%d')}"

    
class VotoContenido(models.Model):
    VOTOS = [
        ('LIKE', 'Like'),
        ('UNLIKE', 'Unlike')
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    tipo_voto = models.CharField(max_length=6, choices=VOTOS)
    fecha_voto = models.DateTimeField(auto_now_add=True)
    
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


#reporte de contenido
class ReporteContenido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usuario que reporta
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)  # Contenido reportado
    razon = models.TextField()  # Motivo del reporte
    fecha_reporte = models.DateTimeField(auto_now_add=True)  # Fecha del reporte

    def __str__(self):
        return f'Reporte de {self.usuario.username} sobre {self.contenido.titulo_conte}'

