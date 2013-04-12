import colander

from kotti.views.slots import assign_slot

from kotti_settings.config import SlotSchemaNode
from kotti_settings.config import ShowInContextSchemaNode
from kotti_settings.util import add_settings
from kotti_settings.util import get_setting
from kotti_grid import _


class GridSchema(colander.MappingSchema):
    slot = SlotSchemaNode(colander.String())
    show_in_context = ShowInContextSchemaNode(colander.String())


GridSettings = {
    'name': 'grid_settings',
    'title': _(u'Grid Settings'),
    'description': _(u"Settings for kotti_grid"),
    'success_message': _(u"Successfully saved kotti_grid settings."),
    'schema_factory': GridSchema,
}


def populate():
    add_settings(GridSettings)
    slot = get_setting('slot', u'belowcontent')
    assign_slot('grid-widget', slot)
