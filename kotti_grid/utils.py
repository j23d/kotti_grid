from kotti.resources import get_root

SETTINGS_KEY = "kotti_grid.settings"


def grid_settings():
    root = get_root()
    if SETTINGS_KEY not in root.annotations:
        init = {'grid': None, 'tiles': []}
        root.annotations[SETTINGS_KEY] = init
    return root.annotations[SETTINGS_KEY]


def save_grid_settings(data, key='grid'):
    grid_settings()[key] = data
    return True
