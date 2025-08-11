
import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


import datetime

current_year = datetime.datetime.now().year

project = 'ICF Specification Guide'
copyright = '2025 - {} , IOBEWI'.format(current_year)
author = 'IOBEWI'
release = '1.0'

extensions = [
    'sphinx_rtd_theme'
]

source_suffix = {
    ".rst": "restructuredtext",
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/iobewi.png'
html_theme_options = {
    'logo_only': True,
    'display_version': True,
}

html_css_files=['custom.css']
html_favicon = '_static/favicon.ico'  # mets ton favicon ici (optionnel)
