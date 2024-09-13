from django.db import migrations

def create_initial_tags(apps, schema_editor):
    Tag = apps.get_model('contenido', 'Tag')
    tags = [
        'Deportes', 'Fútbol', 'Tecnología', 'Ciencia', 'Educación', 'Entretenimiento',
        'Viajes', 'Cocina', 'Moda', 'Salud', 'Belleza', 'Noticias', 'Películas',
        'Series', 'Libros', 'Música', 'Arte', 'Videojuegos', 'Historia', 'Política',
        'Economía', 'Cultura', 'Desarrollo personal', 'Psicología', 'Animales', 'Medio ambiente',
        'Innovación', 'Negocios', 'Marketing', 'Redes sociales', 'Fotografía', 'Programación',
        'Diseño gráfico'
    ]
    
    for tag in tags:
        Tag.objects.create(nombre=tag)

class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0006_contenido_tags'),
    ]

    operations = [
        migrations.RunPython(create_initial_tags),
    ]
