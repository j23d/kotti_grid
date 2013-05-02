import types
import pytest

from kotti.testing import FunctionalTestBase

from kotti_grid.widget import grid_widget


def test_widget_view(kg_populate, db_session, dummy_request, events):
    from kotti.resources import get_root
    root = get_root()
    widget_vals = grid_widget(root, dummy_request)

    assert widget_vals['show'] is True
    assert isinstance(widget_vals['tile_content'], types.FunctionType)
    assert widget_vals['tiles'] == []


def test_not_show_widget(kg_populate, db_session, dummy_request, events):
    from kotti.resources import get_root
    from pyramid.exceptions import PredicateMismatch

    root = get_root()
    settings = root.annotations[u'kotti_settings']
    settings[u'kotti_grid-show_in_context'] = u'not on root'

    with pytest.raises(PredicateMismatch):
        grid_widget(root, dummy_request)


def test_add_tile(db_session, dummy_request, root):
    from kotti_grid.widget import add_tile
    assert add_tile(root, dummy_request) == {}


def test_save_tiles(db_session, dummy_request, root):
    from kotti_grid.views import save_grid
    from kotti_grid.utils import grid_settings
    dummy_request.POST['tiles'] = '{"many": "tiles"}'

    assert save_grid(root, dummy_request) is True

    settings = grid_settings()
    assert settings['tiles'] == {'many': 'tiles'}


def test_tile_content_nourl(db_session, dummy_request, root):
    from kotti_grid.widget import tile_content
    assert tile_content(root, dummy_request) == u""


def test_tile_content_call(db_session, dummy_request, root):
    from kotti_grid.widget import tile_content
    from kotti.resources import Document

    root['doc1'] = Document(title=u'Tile Doc',
                            description=u'I am the doc')

    content = tile_content(root, dummy_request, url='/doc1')
    # here we have to extend the config with our configurator
    assert content is None


class TestTileContent(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_grid.kotti_configure'}
        super(TestTileContent, self).setUp(**settings)

    def test_tile_content_call(self):
        from kotti_grid.widget import tile_content
        from kotti.resources import Document
        from kotti.resources import get_root
        from kotti.testing import DummyRequest

        root = get_root()
        dummy_request = DummyRequest()

        root['doc1'] = Document(title=u'Tile Doc',
                                description=u'I am the doc')
        content = tile_content(root, dummy_request, url='/doc1',
                               use='use_title_and_description')
        assert u'<div class="tile-content"' in content
        assert u'<h4>Tile Doc</h4>' in content
        assert u'<span>I am the doc</span>' in content

    def test_tile_content_request(self):
        from kotti_grid.widget import tile_content
        from kotti.resources import Document
        from kotti.resources import get_root
        from kotti.testing import DummyRequest

        root = get_root()
        dummy_request = DummyRequest()

        root['doc2'] = Document(title=u'Tile Doc 2',
                                description=u'I am the doc 2')
        dummy_request.POST['url'] = '/doc2'
        dummy_request.POST['use'] = 'use_title_and_description'
        dummy_request.POST['size_x'] = '4'
        dummy_request.POST['extra_style'] = 'border: 1px solid blue;'
        content = tile_content(root, dummy_request)
        assert u'<div class="tile-content"' in content
        assert u'<h4>Tile Doc 2</h4>' in content
        assert u'<span>I am the doc 2</span>' in content
        assert u'border: 1px solid blue;' in content

    def test_tile_content_not_exists(self):
        from kotti_grid.widget import tile_content
        from kotti.resources import get_root
        from kotti.testing import DummyRequest

        root = get_root()
        dummy_request = DummyRequest()

        content = tile_content(root, dummy_request, url='/not-existing')
        assert content == u"Can't find resource with path /not-existing."

    def test_tile_content_with_image(self):
        from kotti_grid.widget import tile_content
        from kotti.resources import Document
        from kotti.resources import Image
        from kotti.resources import get_root
        from kotti.testing import DummyRequest
        from kotti import DBSession

        root = get_root()
        dummy_request = DummyRequest()

        root['doc1'] = Document(title=u'Tile with image')
        root['doc1']['image'] = Image("image content",
                                      u"img.png",
                                      u"image/png")
        DBSession.flush()
        content = tile_content(root, dummy_request, url='/doc1',
                               use='use_internal_image')
        assert content is not None
