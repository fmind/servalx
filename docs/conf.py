#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(here, os.pardir))

from setup import AUTHOR, COPYRIGHT, PROJECT, VERSION

# Extensions

extensions = ["sphinx.ext.autodoc"]

# -- General Information ------------------------------------------

language = None
author = AUTHOR
project = PROJECT
version = VERSION
release = VERSION
copyright = COPYRIGHT

# -- General Configuration ------------------------------------------

master_doc = "index"
source_suffix = ".rst"
pygments_style = "sphinx"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output ------------------------------------------

html_theme = "nature"
# html_theme_options = {}
html_static_path = ["_static"]
htmlhelp_basename = project + "doc"

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, "Project Documentation", [author], 1)]

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'a4paper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "project.tex", "Project Documentation", author, "manual")
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        "Project Documentation",
        author,
        project,
        "One line description of project.",
        "Miscellaneous",
    )
]
