# -*- coding: utf-8 -*-
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary'
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.org/en/latest/', None)
}

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyexcel'
copyright = u'2015-2016 Onni Software Ltd.'
version = '0.2.4'
release = '0.2.4'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'


def setup(app):
    app.add_stylesheet('theme_overrides.css')
html_static_path = ['_static']
htmlhelp_basename = 'pyexceldoc'
latex_elements = {}
latex_documents = [
    ('index', 'pyexcel.tex', u'pyexcel Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyexcel', u'pyexcel Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyexcel', u'pyexcel Documentation',
     'Onni Software Ltd.', 'pyexcel', 'One line description of project.',
     'Miscellaneous'),
]
