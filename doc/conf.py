#!/usr/bin/env python3.7
#
# ShiftD documentation build configuration file.
import shiftd


# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = ['.rst']

# source_encoding = 'utf-8-sig'

master_doc = 'index'

# General information about the project.
project = 'ShiftD'
author = 'Alex Kopchikov'
copyright = '2019, {}'.format(author)

# The short X.Y version.
version = shiftd.__version__
# The full version, including alpha/beta/rc tags.
release = shiftd.__release__

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'

html_theme_options = {
    # 'Alabaster' theme configuration.
    'page_width': '75%',
}

html_static_path = ['_static']

html_show_copyright = True


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
     'papersize': 'a4paper',
     # 'pointsize': '10pt',
     # 'preamble': '',
     # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'shiftd.tex', 'ShiftD Documentation', author, 'manual'),
]
