project = 'ruly'
copyright = '2020, Zlatan Sicanica'
author = 'Zlatan Sicanica'

with open('../version.txt') as fh:
    version = fh.read()
release = version


extensions = ['sphinxcontrib.napoleon',
              'sphinx.ext.intersphinx']

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

templates_path = ['_templates']

html_theme = 'nature'

html_static_path = ['_static']
