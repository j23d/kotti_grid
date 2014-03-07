import types
import pytest

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


def test_tile_content_call(db_session, kg_setup, dummy_request, root):
    from kotti_grid.widget import tile_content
    from kotti.resources import Document

    root['doc1'] = Document(title=u'Tile Doc',
                            description=u'I am the doc')
    content = tile_content(root, dummy_request, url='/doc1',
                           use='use_title_and_description')
    assert u'<a class="tile-content"' in content
    assert u'<h4>Tile Doc</h4>' in content
    assert u'<span>I am the doc</span>' in content


def test_tile_content_request(db_session, kg_setup, dummy_request, root):
    from kotti_grid.widget import tile_content
    from kotti.resources import Document

    root['doc2'] = Document(title=u'Tile Doc 2',
                            description=u'I am the doc 2')
    dummy_request.POST['url'] = '/doc2'
    dummy_request.POST['use'] = 'use_title_and_description'
    dummy_request.POST['size_x'] = '4'
    dummy_request.POST['extra_style'] = 'border: 1px solid blue;'
    content = tile_content(root, dummy_request)
    assert u'<a class="tile-content"' in content
    assert u'<h4>Tile Doc 2</h4>' in content
    assert u'<span>I am the doc 2</span>' in content
    assert u'border: 1px solid blue;' in content


def test_tile_content_custom_text(db_session, kg_setup, dummy_request, root):
    from kotti_grid.widget import tile_content
    from kotti.resources import Document

    root['doc3'] = Document(title=u'Tile Doc 3')
    dummy_request.POST['url'] = '/doc3'
    dummy_request.POST['use'] = 'use_custom_text'
    dummy_request.POST['custom_text'] = '<p>this is it</p>'
    dummy_request.POST['size_x'] = '4'
    content = tile_content(root, dummy_request)
    assert u'<a class="tile-content"' in content
    assert u'<p>this is it</p>' in content


def test_tile_content_not_exists(db_session, kg_setup, dummy_request, root):
    from kotti_grid.widget import tile_content

    content = tile_content(root, dummy_request, url='/not-existing')
    assert content == u"Can't find resource with path /not-existing."


def test_tile_content_with_image(db_session, kg_setup, dummy_request, root):
    from zope import interface
    from kotti.interfaces import IDefaultWorkflow
    from kotti_grid.widget import tile_content
    from kotti.resources import Document
    from kotti.resources import Image
    from kotti.workflow import get_workflow

    root[u'doc1'] = Document(title=u'Tile with image')
    root[u'doc1'][u'image'] = Image("image content",
                                    u"img.png",
                                    u"image/png")
    # We have to publish the image to get the permission to view it in this test.
    interface.directlyProvides(root[u'doc1'][u'image'], IDefaultWorkflow)
    wf = get_workflow(root[u'doc1'][u'image'])
    wf.transition_to_state(root[u'doc1'][u'image'], None, u'public')

    content = tile_content(root, dummy_request, url='/doc1',
                           use='use_internal_image')
    assert 'href="http://example.com/doc1/"' in content
    assert 'src="http://example.com/doc1/image/image/span2"' in content
    assert 'title="Tile with image"' in content
