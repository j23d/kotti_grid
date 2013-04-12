from urlparse import urlparse

from pyramid.events import subscriber
from pyramid.traversal import find_resource
from pyramid.view import view_config

from kotti.resources import get_root
from kotti.views.slots import assign_slot
from kotti.views.slots import objectevent_listeners
from kotti.views.slots import slot_events
from kotti.views.util import render_view

from kotti_settings.config import slot_names
from kotti_settings.events import SettingsAfterSave
from kotti_settings.util import get_setting

from kotti_grid.utils import grid_settings


@view_config(name='grid-widget',
             renderer='kotti_grid:templates/grid.pt')
def grid_widget(context, request):
    show_in_context = get_setting(u'show_in_context')
    show = False
    if show_in_context == u'everywhere':
        show = True
    elif show_in_context == u'only on root':
        show = context == get_root()
    elif show_in_context == u'not on root':
        show = context != get_root()
    elif show_in_context == u'nowhere':
        show = False
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


@subscriber(SettingsAfterSave)
def set_assigned_slot(event):
    """Reset the widget to the choosen slot."""

    # Check if the settings for this module was saved.
    if not event.module == __package__:
        return

    slot = get_setting('slot', u'left')
    names = [name[0] for name in slot_names]

    # This is somewhat awkward. We check all slots if the widget is already
    # set and remove it from the listener before we set it to another one.
    for slot_event in slot_events:
        if slot_event.name not in names:
            continue
        try:
            listener = objectevent_listeners[(slot_event, None)]
        except TypeError:
            listener = None
        if listener is not None:
            for func in listener:
                if func.func_closure[1].cell_contents == 'grid-widget':
                    listener.remove(func)
    assign_slot('grid-widget', slot)


def includeme(config):
    config.scan(__name__)
