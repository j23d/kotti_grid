from pyramid.interfaces import ITranslationDirectories

from kotti_grid import includeme
from kotti_grid import kotti_configure


def test_kotti_configure():

    settings = {
        'kotti.available_types': '',
        'pyramid.includes': '',
        'kotti.fanstatic.view_needed': '',
    }

    kotti_configure(settings)

    assert settings['pyramid.includes'] ==\
        ' kotti_grid kotti_grid.widget kotti_grid.views'
    assert settings['kotti.fanstatic.view_needed'] ==\
        ' kotti_grid.fanstatic.kotti_grid'


def test_includeme(config):

    includeme(config)

    utils = config.registry.__dict__['_utility_registrations']
    k = (ITranslationDirectories, u'')

    # test if the translation dir is registered
    assert k in utils
    assert utils[k][0][0].find('kotti_grid/locale') > 0
