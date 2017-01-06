# -*- coding: utf-8 -*-

import os
import sys

src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
src_dir = os.path.abspath(src_dir)

sys.path.insert(1, src_dir)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'PyCodebase'
copyright = u'2017, David Buxton'
author = u'David Buxton'

# The short X.Y version.
version = u'0.2'
# The full version, including alpha/beta/rc tags.
release = u'0.2'

language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build']

pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'PyCodebasedoc'
