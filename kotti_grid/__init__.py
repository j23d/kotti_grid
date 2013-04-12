from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_grid')


def kotti_configure(settings):
    settings['pyramid.includes'] +=\
        ' kotti_grid kotti_grid.widget kotti_grid.views'
    settings['kotti.fanstatic.view_needed'] +=\
        ' kotti_grid.fanstatic.kotti_grid'
    settings['kotti.populators'] += ' kotti_grid.populate.populate'


def includeme(config):
    config.add_translation_dirs('kotti_grid:locale')
