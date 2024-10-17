from django.db import models
from categorias.models import Categoria  # Importa el modelo Categoria
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone
from .models import Categoria
from django.utils.html import strip_tags


class Tag(models.Model):
    '''
    @class Tag
    @extends models.Model
    @description Modelo que representa una etiqueta (tag) asociada al contenido. Cada etiqueta tiene un nombre único con un límite de 50 caracteres.
    '''
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
    vigencia_conte = models.BooleanField(default=False)
    

    # Relación con el autor del contenido
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,  # Si el autor es eliminado, se establece en NULL
        null=True, 
        blank=True
    )
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_vigencia = models.DateTimeField(null=True, blank=True)
    
    
     # Campo para almacenar la versión actual seleccionada
    version_actual = models.ForeignKey(
        'VersionContenido',  # Relacionado con el modelo de versiones
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contenido_version_actual'
    )

    def __str__(self):
        return self.titulo_conte
    
    def establecer_version_actual(self, version):
        """Establece una versión específica como la versión actual del contenido."""
        self.version_actual = version
        self.save()
        
    def establecer_version_anterior(self, version):
        """
        Este método permite establecer cualquier versión anterior como la versión actual.
        Primero, guarda la versión actual antes de cambiarla para evitar perderla.
        """
        # Si hay una versión actual, guárdala como una nueva versión
        if self.version_actual:
            version_num = self.versiones.count() + 1  # Crear el siguiente número de versión
            VersionContenido.objects.create(
                contenido_original=self,
                version_num=version_num,
                titulo_conte=self.titulo_conte,
                tipo_conte=self.tipo_conte,
                texto_conte=self.texto_conte,
                fecha_version=timezone.now(),
            )

        # Ahora, establece la versión seleccionada como la actual
        self.titulo_conte = version.titulo_conte
        self.tipo_conte = version.tipo_conte
        self.texto_conte = version.texto_conte
        self.version_actual = version  # Establecemos la nueva versión como la actual
        self.save()  # Guardamos los cambios
    
        # Método para verificar si el contenido debe ser publicado
    def autopublicar(self):
        if self.fecha_publicacion and self.fecha_publicacion <= timezone.now() and self.estado_conte == 'PUBLICADO':
            self.autopublicar_conte = True
            self.save()
            
    def save(self, *args, crear_version=True, **kwargs):
        """
        Sobrescribe el método save para crear una nueva versión solo cuando `crear_version` es True.
        """
        is_new = self.pk is None  # Verificar si es un nuevo contenido

        # Si es una edición, obtenemos el estado original antes de guardar
        if not is_new:
            try:
                original = Contenido.objects.get(pk=self.pk)
            except Contenido.DoesNotExist:
                original = None
        else:
            original = None

        # Guardamos el contenido primero (si es un nuevo contenido)
        super(Contenido, self).save(*args, **kwargs)

        if is_new:
            # Si es un nuevo contenido, crear la versión 1
            print("Creando la versión 1 del contenido")
            version = VersionContenido.objects.create(
                contenido_original=self,
                version_num=1,
                titulo_conte=self.titulo_conte,
                tipo_conte=self.tipo_conte,
                texto_conte=self.texto_conte,
                fecha_version=timezone.now(),
            )

            # Establecer la versión 1 como la versión actual
            self.version_actual = version
            self.save()  # Guardar nuevamente para asignar la versión actual
            print(f"Versión 1 creada y asignada como la versión actual: {self.version_actual}")

        elif original and crear_version:
            # Solo creamos una nueva versión si `crear_version` es True
            print(f"Comparando texto_conte (sin HTML):")
            print(f"Original (limpio): {strip_tags(original.texto_conte)}")
            print(f"Nuevo (limpio): {strip_tags(self.texto_conte)}")

            print(f"Comparando titulo_conte:")
            print(f"Original: {original.titulo_conte}")
            print(f"Nuevo: {self.titulo_conte}")

            # Comparar si hubo cambios significativos en el título o texto sin HTML
            if strip_tags(original.texto_conte) != strip_tags(self.texto_conte) or original.titulo_conte != self.titulo_conte:
                print("Detectados cambios en el contenido, creando una nueva versión")
                # Incrementar el número de versión basado en las versiones existentes
                version_num = self.versiones.count() + 1
                version = VersionContenido.objects.create(
                    contenido_original=self,
                    version_num=version_num,
                    titulo_conte=self.titulo_conte,  # Guardar el título editado
                    tipo_conte=self.tipo_conte,      # Guardar el tipo editado
                    texto_conte=self.texto_conte,    # Guardar el texto editado
                    fecha_version=timezone.now(),    # Guardar la fecha de edición
                )

                # Establecer la nueva versión creada como la versión actual
                self.version_actual = version
                self.save()  # Guardar nuevamente para asignar la versión actual
                print(f"Versión {version_num} creada y asignada como la versión actual: {self.version_actual}")
            else:
                print("No se detectaron cambios significativos, no se crea una nueva versión")



    
class VersionContenido(models.Model):
    '''
    @class VersionContenido
    @extends models.Model
    @description Modelo que almacena versiones de un contenido original. Cada versión está vinculada a un contenido original y contiene información como el número de versión, título, tipo, texto y la fecha en la que fue creada.
    '''
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
    '''
    @class VotoContenido
    @extends models.Model
    @description Modelo que representa un voto de un usuario sobre un contenido. Un voto puede ser un 'Like' o 'Unlike' y cada usuario solo puede votar una vez por contenido.
    '''
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
    '''
    @class Suscripcion
    @extends models.Model
    @description Modelo que representa la suscripción de un usuario a una categoría específica. Un usuario puede suscribirse a varias categorías, pero solo una vez por cada categoría.
    '''
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.categoria.nombre}"
    
    class Meta:
        unique_together = ('usuario', 'categoria')  # Evita duplicados de suscripciones


#reporte de contenido
class ReporteContenido(models.Model):
    '''
    @class ReporteContenido
    @extends models.Model
    @description Modelo que representa un reporte realizado por un usuario sobre un contenido. Cada reporte contiene el usuario que lo realizó, el contenido reportado, el motivo del reporte y la fecha en la que fue creado.
    '''
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usuario que reporta
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)  # Contenido reportado
    razon = models.TextField()  # Motivo del reporte
    fecha_reporte = models.DateTimeField(auto_now_add=True)  # Fecha del reporte

    def __str__(self):
        return f'Reporte de {self.usuario.username} sobre {self.contenido.titulo_conte}'


#historial de compra de categorías 
class HistorialCompra(models.Model):
    '''
    @class HistorialCompra
    @extends models.Model
    @description Modelo que almacena el historial de compras realizadas por los usuarios. Incluye detalles como el usuario que realizó la compra, el número de la compra, la categoría relacionada y la fecha de la transacción.
    '''
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_compra = models.CharField(max_length=100)  # Número o ID de la compra de Stripe
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)  # Fecha de la compra

    def __str__(self):
        return f"Compra {self.numero_compra} - {self.categoria.nombre}"


class CambioEstado(models.Model):
    '''
    @class CambioEstado
    @extends models.Model
    @description Modelo que registra los cambios de estado de un contenido. Almacena información sobre el contenido afectado, el estado anterior, el nuevo estado, el usuario que realizó el cambio, la fecha y las razones asociadas.
    '''
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='cambios_estado')
    estado_anterior = models.CharField(max_length=50)
    estado_nuevo = models.CharField(max_length=50)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    razon_cambio = models.TextField(blank=True, null=True)  # Solo para cambios a "Borrador"
    razon_revision = models.TextField(blank=True, null=True)  # Solo para cambios a "En revision"
    

    def _str_(self):
        return f"Cambio en {self.contenido.titulo_conte} de {self.estado_anterior} a {self.estado_nuevo}"
    

# Calificación de estrellas

class Rating(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    estrellas = models.IntegerField(default=0)  # Rating de 1 a 5 estrellas
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'contenido')  # Un usuario solo puede calificar un contenido una vez

    def __str__(self):
        return f'{self.usuario} - {self.contenido}: {self.estrellas} estrellas'
