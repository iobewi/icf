
import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'ICF Specification'
copyright = '2025, IOBEWI'
author = 'IOBEWI'
release = '1.0'

extensions = [
    'myst_parser',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/iobewi.png'
html_theme_options = {
    'logo_only': True,
    'display_version': True,
}
