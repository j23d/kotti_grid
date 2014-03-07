

def test_gridbrowser_view(db_session, dummy_request, root):
    from kotti_grid.views import GridBrowser
    gt = GridBrowser(root, dummy_request)
    browser = gt.gridbrowser()
    assert browser['form'].startswith('<form')


def test_grid_settings_view(db_session, dummy_request, root):
    from kotti_grid.views import grid_settings
    view = grid_settings(root, dummy_request)
    assert view == {'width': 150, 'margin_y': 10,
                    'margin_x': 10, 'resize_tiles': False,
                    'height': 150, 'slot': 'belowcontent'}
