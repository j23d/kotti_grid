from urlparse import urlparse

from pyramid.events import subscriber
from pyramid.traversal import find_resource
from pyramid.view import view_config

from kotti.interfaces import IImage
from kotti.resources import get_root
from kotti.views.slots import assign_slot
from kotti.views.slots import objectevent_listeners
from kotti.views.slots import slot_events
from kotti.views.util import nodes_tree
from kotti.views.util import render_view

from kotti_settings.config import slot_names
from kotti_settings.events import SettingsAfterSave
from kotti_settings.util import get_setting

from kotti_grid.utils import grid_settings
from kotti_grid import _


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
            'show': show,
            'dimension_x': get_setting(u'dimension_x', 150),
            'dimension_y': get_setting(u'dimension_y', 150),
            'margin_x': get_setting(u'margin_x', 10),
            'margin_y': get_setting(u'margin_y', 10)}


@view_config(name="tile-content", renderer='string')
def tile_content(context, request, url=None, size_x=None, use=None,
                 extra_style=None):
    if url is None and 'url' in request.POST:
        url = request.POST['url']
    if use is None and 'use' in request.POST:
        use = request.POST['use']
    if extra_style is None and 'extra_style' in request.POST:
        extra_style = request.POST['extra_style']
    if url is None:
        return u''
    if size_x is None and 'size_x' in request.POST:
        size_x = request.POST['size_x']
    path = urlparse(url).path
    try:
        resource = find_resource(context, path)
    except KeyError:
        return _(u"Can't find resource with path {0}.".format(path))

    request.image = None
    if use == u'use_internal_image':
        tree = nodes_tree(request, context=resource).tolist()
        if tree:
            resource_images = [obj for obj in tree if IImage.providedBy(obj)]
            if resource_images:
                request.image = resource_images[0]

    request.content_url = request.resource_url(resource)

    request.view_name = "tile-view"
    request.size = 2
    if size_x:
        request.size = int(size_x) + 2
    request.use = None
    if use is not None:
        request.use = use
    request.extra_style = u''
    if extra_style is not None:
        request.extra_style = extra_style
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
