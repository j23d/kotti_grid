from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery import jquery

from js.jquery_colorpicker import jquery_colorpicker
from js.gridster import gridster


library = Library('kotti_grid', 'static')

css = Resource(library, 'css/style.css',
               minified='css/style.min.css')


js = Resource(library, "js/script.js",
              minified="js/script.min.js",
              depends=[jquery, jquery_colorpicker, gridster])

kotti_grid = Group([css, js, ])
