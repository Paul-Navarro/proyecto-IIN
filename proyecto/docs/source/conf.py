
import os
import sys
import django

# Insertar la ruta del directorio en sys.path
sys.path.insert(0, r'/home/fabel/code/facu/is2/proyecto-IIN/proyecto')
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CMS_grupo_05'
copyright = '2024, Crista, Maria José, Paul, Diego, Javier'
author = 'Crista, Maria José, Paul, Diego, Javier'

version = '1.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
