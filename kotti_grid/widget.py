from urlparse import urlparse

from pyramid.traversal import find_resource
from pyramid.view import view_config

from kotti.resources import get_root
from kotti.views.slots import assign_slot
from kotti.views.util import render_view

from kotti_grid.utils import grid_settings


@view_config(name='grid-widget',
             renderer='kotti_grid:templates/grid.pt')
def grid_widget(context, request):
    show = context == get_root()
    if show:
        from js.jquery_colorpicker import jquery_colorpicker
        from js.gridster import gridster
        jquery_colorpicker.need()
        gridster.need()
    return {'tiles': grid_settings()['tiles'],
            'tile_content': tile_content,
            'show': show}


@view_config(name="tile-content", renderer='string')
def tile_content(context, request, url=None, size_x=None):
    if url is None and 'url' in request.GET:
        url = request.GET['url']
    if url is None:
        return u''
    if size_x is None and 'size_x' in request.GET:
        size_x = request.GET['size_x']
    path = urlparse(url).path
    resource = find_resource(context, path)
    request.view_name = "tile-view"
    request.size = 2
    if size_x:
        request.size = int(size_x) + 2
    return render_view(resource, request, name="tile-view")


@view_config(name="tile-view",
             renderer="kotti_grid:templates/tile-view.pt")
def tile_view(context, request):
    return {}


@view_config(name="add-tile",
             renderer="kotti_grid:templates/add-tile.pt")
def add_tile(context, request):
    return {}


def includeme(config):
    config.scan(__name__)
    assign_slot('grid-widget', u'belowcontent')
