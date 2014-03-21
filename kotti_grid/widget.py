from urlparse import urlparse

from pyramid.events import subscriber
from pyramid.exceptions import PredicateMismatch
from pyramid.traversal import find_resource
from pyramid.view import view_config

from kotti.interfaces import IImage
from kotti.views.slots import assign_slot
from kotti.views.slots import objectevent_listeners
from kotti.views.slots import slot_events
from kotti.views.util import nodes_tree
from kotti.views.util import render_view

from kotti_settings.config import slot_names
from kotti_settings.events import SettingsAfterSave
from kotti_settings.util import get_setting
from kotti_settings.util import remove_from_slots
from kotti_settings.util import show_in_context

from kotti_grid.fanstatic import kotti_grid
from kotti_grid.utils import grid_settings
from kotti_grid import _


@view_config(name='grid-widget',
             renderer='kotti_grid:templates/grid.pt')
def grid_widget(context, request):
    show = show_in_context(get_setting(u'show_in_context'), context)
    if show:
        kotti_grid.need()
        return {'tiles': grid_settings()['tiles'],
                'tile_content': tile_content,
                'show': show,
                'width': get_setting(u'width', 150),
                'height': get_setting(u'height', 150),
                'margin_x': get_setting(u'margin_x', 10),
                'margin_y': get_setting(u'margin_y', 10)}
    raise(PredicateMismatch)


@view_config(name="tile-content", renderer='string')
def tile_content(context, request, url=None, size_x=None, use=None,
                 custom_text=None, extra_style=None):
    if url is None and 'url' in request.POST:
        url = request.POST['url']
    if use is None and 'use' in request.POST:
        use = request.POST['use']
    if custom_text is None and 'custom_text' in request.POST:
        custom_text = request.POST['custom_text']
    if extra_style is None and 'extra_style' in request.POST:
        extra_style = request.POST['extra_style']
    if size_x is None and 'size_x' in request.POST:
        size_x = request.POST['size_x']

    if url == '' or url is None or url is False:
        request.content_url = None
        current_context = context
    else:
        resource = None
        app_url = request.application_url
        parsed_url = urlparse(url)
        base_url = "{}://{}".format(parsed_url.scheme, parsed_url.netloc)
        if app_url.startswith(base_url) or url.startswith('/'):
            try:
                resource = find_resource(context, parsed_url.path)
            except KeyError:
                return _(u"Can't find resource with path {0}.".format(parsed_url.path))

        request.image = None
        if resource is not None:
            current_context = resource
            if use == u'use_internal_image':
                tree = nodes_tree(request, context=resource).tolist()
                if tree:
                    resource_images = [obj for obj in tree if IImage.providedBy(obj)]
                    if resource_images:
                        request.image = resource_images[0]
            request.content_url = request.resource_url(resource)
            request.target = '_self'
        else:
            current_context = context
            request.content_url = url
            request.target = '_blank'

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
    if custom_text is not None:
        request.custom_text = custom_text
    return render_view(current_context, request, name="tile-view")


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
    if not event.module == __package__:  # pragma: no cover
        return

    slot = get_setting('slot', u'left')
    names = [name[0] for name in slot_names]

    remove_from_slots('grid-widget')
    assign_slot('grid-widget', slot)


def includeme(config):
    config.scan(__name__)
