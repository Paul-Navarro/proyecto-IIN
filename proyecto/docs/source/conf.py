# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django
sys.path.insert(0, os.path.abspath('C:\\Users\\user\\Desktop\\pis2\\proyecto-IIN\\proyecto'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyecto.settings'
django.setup()
project = 'CMS_grupo_05'
copyright = '2024, Crista, Maria José, Paul, Diego, Javier'
author = 'Crista, Maria José, Paul, Diego, Javier'
release = 'es'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary', 
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_sidebars = { '': ['globaltoc.html', 'relations.html','sourcelink.html', 'searchbox.html'],}