from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti.fanstatic import edit_needed
from kotti.interfaces import IContent

from kotti_grid.fanstatic import kotti_grid
from kotti_grid.utils import save_grid_settings

from kotti_grid import _


@view_config(name="save-grid", permission="edit",
             request_method="POST", renderer="json")
def save_grid(context, request):
    data = request.POST
    tiles = eval(data['tiles'])
    request.session.flash(
        _(u'The tiles have been saved.'), 'success')
    return save_grid_settings(tiles, 'tiles')


@view_defaults(context=IContent,
               request_method="GET")
class GridBrowser():

    def __init__(self, context, request):

        self.context = context
        self.request = request

    @view_config(name="gridbrowser",
                 renderer="kotti_grid:templates/browser.pt")
    def gridbrowser(self):
        return {}


def includeme(config):
    config.scan(__name__)
    edit_needed.add(kotti_grid)
