import ruly.version

project = 'ruly'
copyright = '2020, Zlatan Sicanica'
author = 'Zlatan Sicanica'

release = ruly.version.version


extensions = ['sphinxcontrib.napoleon',
              'sphinx.ext.intersphinx']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

templates_path = ['_templates']

html_theme = 'nature'

html_static_path = ['_static']
