from datetime import datetime
import importlib.metadata


project = "ruly"
author = "Zlatan Sičanica"
copyright = f"{datetime.today().year}, {author}"
version = importlib.metadata.version(project)
release = version


extensions = ["sphinx.ext.napoleon", "sphinx.ext.intersphinx"]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ["_templates"]

html_theme = "nature"

html_static_path = ["_static"]
