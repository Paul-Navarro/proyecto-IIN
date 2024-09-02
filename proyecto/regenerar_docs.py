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
django_config = """
import os
import sys
import django

sys.path.insert(0, os.path.abspath(r'C:\\Users\\HOME\\Desktop\\ProyectoIs2\\proyecto-IIN\\proyecto'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'
django.setup()
"""

# Insertar las configuraciones de Django al inicio de conf.py
with open(conf_py_path, 'r+') as conf_file:
    content = conf_file.read()
    conf_file.seek(0, 0)
    conf_file.write(django_config + '\n' + content)
    print("Configuración de Django añadida a conf.py.")

# 7. Agregar módulos a index.rst
modules_to_add = """
   modules/categorias
   modules/contenido
   modules/users
   modules/proyecto
   modules/manage
   modules/modules
"""

with open(index_rst_path, 'a') as index_file:
    index_file.write("\n" + modules_to_add)
    print("Módulos añadidos a index.rst.")

# 8. Construir la documentación en HTML usando make.bat
subprocess.run(['make.bat', 'html'])

# Asegurarse de que no haya una carpeta 'docs' duplicada después de la construcción de la documentación
eliminar_docs_duplicado()

print("Documentación generada exitosamente.")
