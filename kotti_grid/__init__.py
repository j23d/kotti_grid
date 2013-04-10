from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_grid')


_ = TranslationStringFactory('{{{ package.name }}}')


def kotti_configure(settings):
    settings['pyramid.includes'] +=\
        ' kotti_grid kotti_grid.widget kotti_grid.views'
    settings['kotti.fanstatic.view_needed'] +=\
        ' kotti_grid.fanstatic.kotti_grid'


def includeme(config):
    config.add_translation_dirs('kotti_grid:locale')
