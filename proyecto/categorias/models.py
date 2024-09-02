from django.db import models

class Categoria(models.Model):
    """
    @class Categoria
    @extends models.Model
    @description Modelo que representa una categoría en el sistema.
    Este modelo define una categoría con atributos como nombre, estado de moderación, estado de pago, accesibilidad para suscriptores, y un código único.
    También maneja la autogeneración del código si no se proporciona uno.
    """
    nombre = models.CharField(max_length=100)
    es_moderada = models.BooleanField(default=False)
    es_pagada = models.BooleanField(default=False)
    para_suscriptores = models.BooleanField(default=False)
    codigo = models.IntegerField(unique=True, blank=True, null=True)  # Cambia a IntegerField
    tipo_contenido = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.codigo is None:
            # Autogenera un código basado en el ID del último registro o establece en 1 si no hay registros
            last_codigo = Categoria.objects.all().order_by('codigo').last()
            if last_codigo is not None:
                self.codigo = last_codigo.codigo + 1
            else:
                self.codigo = 1
        super(Categoria, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
