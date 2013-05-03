

def test_save_grid_settings(db_session, kg_setup, root):
    from kotti_grid.utils import save_grid_settings
    from kotti_grid.utils import grid_settings

    settings = grid_settings()
    assert settings == {'tiles': [], 'grid': None}

    save_grid_settings(data='My data.', key='a_key')
    assert grid_settings()['a_key'] == 'My data.'
