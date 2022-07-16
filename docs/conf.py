# -- Path Setup -----------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project Information --------------------------------------------

project = 'RegRalXact'
copyright = '2022, allRisc'
author = 'allRisc'

# Full Version
from r2x import VERSION
release = VERSION

# Root document
master_doc = 'index'

# -- General Configuration ------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML Output Options --------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_static_path = []