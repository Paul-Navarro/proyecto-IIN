import os
import shutil
import subprocess

# Ruta del directorio del proyecto y de la carpeta docs
project_dir = os.getcwd()  # Asumiendo que estás en la raíz del proyecto
docs_dir = os.path.join(project_dir, 'docs')
source_dir = os.path.join(docs_dir, 'source')
modules_dir = os.path.join(source_dir, 'modules')
conf_py_path = os.path.join(source_dir, 'conf.py')
index_rst_path = os.path.join(source_dir, 'index.rst')

def eliminar_docs_duplicado():
    # Verificar y eliminar la carpeta docs duplicada si existe
    duplicate_docs_dir = os.path.join(docs_dir, 'docs')
    if os.path.exists(duplicate_docs_dir):
        shutil.rmtree(duplicate_docs_dir)
        print(f"Carpeta duplicada '{duplicate_docs_dir}' eliminada.")

# 1. Eliminar la carpeta docs si existe
if os.path.exists(docs_dir):
    shutil.rmtree(docs_dir)
    print(f"Carpeta '{docs_dir}' eliminada.")

# 2. Crear la estructura de Sphinx
os.makedirs(docs_dir)
os.chdir(docs_dir)

# 3. Inicializar Sphinx
subprocess.run([
    'sphinx-quickstart', 
    '-q', 
    '-p', 'CMS_grupo_05', 
    '-a', 'Crista, Maria José, Paul, Diego, Javier', 
    '-v', '1.0', 
    '-r', '1.0.0', 
    '--sep', 
    '--makefile', 
    '--batchfile', 
    '--extensions=sphinx.ext.autodoc,sphinx.ext.napoleon,sphinx.ext.viewcode'
])

# Asegurarse de que no haya una carpeta 'docs' duplicada dentro de 'docs'
eliminar_docs_duplicado()

# 4. Crear la carpeta modules dentro de source
os.makedirs(modules_dir)

# 5. Regenerar la documentación usando sphinx-apidoc y colocando los .rst en modules
subprocess.run(['sphinx-apidoc', '-o', modules_dir, '..'])

# Asegurarse de que no haya una carpeta 'docs' duplicada dentro de 'docs' después de sphinx-apidoc
eliminar_docs_duplicado()

# 6. Modificar conf.py para integrar Django
# Obtener la ruta del archivo actual
ruta_actual = os.path.abspath(__file__)
# Obtener el directorio donde está el archivo
directorio_actual = os.path.dirname(ruta_actual)
# Reemplazar las barras invertidas simples por dobles
directorio_escapado = directorio_actual.replace('\\', '\\\\')

# Ahora insertamos directorio_escapado en la configuración de Django
django_config = """
import os
import sys
import django

# Insertar la ruta del directorio en sys.path
sys.path.insert(0, r'{}')
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'
django.setup()
""".format(directorio_escapado)  # Aquí insertamos la ruta escapada correctamente


# Insertar las configuraciones de Django al inicio de conf.py
with open(conf_py_path, 'r+') as conf_file:
    content = conf_file.read()
    conf_file.seek(0, 0)
    conf_file.write(django_config + '\n' + content)
    print("Configuración de Django añadida a conf.py.")

# 7. Modificar el archivo index.rst para asegurar que los módulos se incluyan correctamente
index_content = """
Welcome to CMS_grupo05's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/categorias
   modules/contenido
   modules/users
   modules/proyecto
   modules/manage
   modules/modules

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

with open(index_rst_path, 'w') as index_file:
    index_file.write(index_content)
    print("Contenido de index.rst modificado correctamente.")

# 8. Construir la documentación en HTML usando make.bat
subprocess.run(['make', 'html'])#.bat

# Asegurarse de que no haya una carpeta 'docs' duplicada después de la construcción de la documentación
eliminar_docs_duplicado()

print("Documentación generada exitosamente.")
