from django_cron import CronJobBase, Schedule
from .models import Contenido
from django.utils import timezone

class AutopublicarContenido(CronJobBase):
    '''
    @class AutopublicarContenido
    @extends CronJobBase
    @description Clase que se encarga de la tarea de autopublicar contenido programado en base a fechas específicas. Esta tarea se ejecuta periódicamente según la configuración del cron job.
    '''
    RUN_EVERY_MINS = 1  # Cambia este valor según la frecuencia con la que deseas ejecutar la tarea.

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'contenido.autopublicar_contenido'  # Un código único

    def do(self):
        '''
        @function do
        @description Método principal que se ejecuta cada vez que el cron job es disparado. Se encarga de autopublicar los contenidos cuya fecha de publicación ha llegado y de marcar como vigentes los contenidos cuya fecha de vigencia ha sido alcanzada.
        @returns None
        '''
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
        
        contenidos_con_vigencia = Contenido.objects.filter(fecha_vigencia__lte=hora_actual, vigencia_conte=False , estado_conte='PUBLICADO')
        print(f"Contenidos cuya fecha de vigencia ha llegado: {contenidos_con_vigencia.count()}")

        print(f"Contenidos a publicar: {contenidos_a_publicar.count()}")
        
        # Mostrar detalles de cada contenido y actualizar su estado de vigencia
        for contenido in contenidos_con_vigencia:
            print(f"Fecha de vigencia de '{contenido.titulo_conte}': {contenido.fecha_vigencia}")
            contenido.vigencia_conte = True  # Marcar el contenido como vigente
            contenido.save()
            print(f"Contenido '{contenido.titulo_conte}' marcado como vigente.")

        # Mostrar la fecha y hora de cada contenido
        for contenido in contenidos_a_publicar:
            print(f"Fecha de publicación de '{contenido.titulo_conte}': {contenido.fecha_publicacion}")
            print(f"Hora actual: {hora_actual}")
            contenido.autopublicar()
            print(f"Contenido '{contenido.titulo_conte}' autopublicado.")

