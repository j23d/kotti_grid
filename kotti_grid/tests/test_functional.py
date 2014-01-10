from kotti.testing import user
from kotti.testing import BASE_URL


@user('admin')
def test_grid_widget(kg_browser, kg_populate):
    kg_browser.open(BASE_URL)
    assert '<input type="hidden" id="grid-fieldname"' in kg_browser.contents
    assert '<div class="gridster">' in kg_browser.contents
    assert '<button id="save-tiles" class="btn">Save tiles</button>' \
        in kg_browser.contents
    assert '<span id="add-tile" class="tile-action icon-plus">' \
        in kg_browser.contents


@user('admin')
def test_grid_settings(kg_browser, kg_populate):
    ctlr = kg_browser.getControl
    kg_browser.open(BASE_URL + '/@@settings')

    assert 'name="__formid__" value="kotti_grid-grid_settings"' \
        in kg_browser.contents
    assert '<span>Settings for kotti_grid</span>' in kg_browser.contents
    assert 'Height' in kg_browser.contents
    assert 'name="kotti_grid-height" value="150"' in kg_browser.contents

    ctlr(name='kotti_grid-height', index=0).value = '300'
    ctlr(name='save_kotti_grid-grid_settings', index=0).click()
    assert 'name="kotti_grid-height" value="300"' in kg_browser.contents
