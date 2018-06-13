#!/usr/bin/env python3

extensions = []

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "dependencies"
copyright = "2016-2018, Artem Malyshev"
author = "Artem Malyshev"

version = "0.14"
release = "0.14"

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

todo_include_todos = False

html_theme = "alabaster"

html_static_path = ["static"]

html_sidebars = {"**": ["globaltoc.html", "relations.html", "searchbox.html"]}

htmlhelp_basename = "dependenciesdoc"
