# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys

# -- Project information -----------------------------------------------------

project = 'PHYTEC phyHUB Documentation'
copyright = '2026, PHYTEC Messtechnik GmbH'
author = 'PHYTEC'

# Use git describe to get the version e.g.: imx8-pd23.1.0-1-gb1830e
version = re.sub('', '', os.popen('git describe --tags').read().strip())

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx_rtd_theme',
    'sphinx_substitution_extensions',
    'sphinx_sitemap',
    'sphinxcontrib.rsvgconverter',
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '**/README.rst',
]

highlight_language = 'none'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = 'sphinx/static/logo-phytec.svg'
html_favicon = 'sphinx/static/favicon.ico'
html_title = 'PHYTEC phyHUB Documentation'
html_show_sphinx = False
html_baseurl = 'https://phytec.github.io/doc-phyhub/'

# Add robots.txt so search engines can index the site
html_extra_path = ['sphinx/static/robots.txt']

# Link scheme
sitemap_url_scheme = "{link}"
# When adding a lang prefix, this would also affect the english version, which
# currently does not have a language prefix as it is the default. Therefore, we
# currently only support a sitemap without alternative links.
sitemap_locales = [None]

html_theme_options = {
    'logo_only': False,
    'navigation_depth': 5,
}

pages_root = "https://phytec.github.io/doc-phyhub"
html_context = {
    "display_github": True,
    "github_user": "phytec",
    "github_repo": "doc-phyhub",
    "github_version": "main",
    "conf_py_path": "/source/",
    # Language selector, works together with versions.html in templates
    'languages': [
        ['en', pages_root],
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphinx/static']

# The templates directory is used to display a language selector in the sidebar.
templates_path = ['sphinx/templates']

html_css_files = [
    'css/phytec-theme.css',
]

pygments_style = 'bw'
