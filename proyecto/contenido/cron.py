from django_cron import CronJobBase, Schedule
from .models import Contenido
from django.utils import timezone

class AutopublicarContenido(CronJobBase):
    RUN_EVERY_MINS = 1  # Cambia este valor según la frecuencia con la que deseas ejecutar la tarea.

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'contenido.autopublicar_contenido'  # Un código único

    def do(self):
        print("Ejecutando cronjob de autopublicación")
        # Obtener la hora actual
        hora_actual = timezone.now()
        print(f"Hora actual: {hora_actual}")

        # Filtrar contenidos que estén programados para publicarse
        contenidos_a_publicar = Contenido.objects.filter(
            estado_conte='PUBLICADO',
            fecha_publicacion__lte=hora_actual,
            autopublicar_conte=False
        )

        print(f"Contenidos a publicar: {contenidos_a_publicar.count()}")

        # Mostrar la fecha y hora de cada contenido
        for contenido in contenidos_a_publicar:
            print(f"Fecha de publicación de '{contenido.titulo_conte}': {contenido.fecha_publicacion}")
            print(f"Hora actual: {hora_actual}")
            contenido.autopublicar()
            print(f"Contenido '{contenido.titulo_conte}' autopublicado.")
