

def test_gridbrowser(db_session, dummy_request, root):
    from kotti_grid.views import GridBrowser
    gt = GridBrowser(root, dummy_request)
    browser = gt.gridbrowser()
    assert browser == {}
