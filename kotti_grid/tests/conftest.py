from pytest import fixture

pytest_plugins = "kotti"


@fixture
def kg_populate(db_session):
    from kotti_grid.populate import populate
    populate()


def settings():
    from kotti import _resolve_dotted
    from kotti import conf_defaults
    settings = conf_defaults.copy()
    settings['kotti.secret'] = 'secret'
    settings['kotti.secret2'] = 'secret2'
    settings['kotti.configurators'] = \
        'kotti_grid.kotti_configure kotti_settings.kotti_configure'
    settings['kotti.populators'] = 'kotti.testing._populator'
    _resolve_dotted(settings)
    return settings


def setup_app():
    from kotti import base_configure
    return base_configure({}, **settings()).make_wsgi_app()


@fixture
def kg_browser(db_session, request):
    """ returns an instance of `zope.testbrowser`.  The `kotti.testing.user`
        pytest marker (or `pytest.mark.user`) can be used to pre-authenticate
        the browser with the given login name: `@user('admin')`.
    """
    from wsgi_intercept import add_wsgi_intercept, zope_testbrowser
    from kotti.testing import BASE_URL
    host, port = BASE_URL.split(':')[-2:]
    add_wsgi_intercept(host[2:], int(port), setup_app)
    browser = zope_testbrowser.WSGI_Browser(BASE_URL + '/')
    if 'user' in request.keywords:
        # set auth cookie directly on the browser instance...
        from pyramid.security import remember
        from pyramid.testing import DummyRequest
        login = request.keywords['user'].args[0]
        environ = dict(HTTP_HOST=host[2:])
        for _, value in remember(DummyRequest(environ=environ), login):
            cookie, _ = value.split(';', 1)
            name, value = cookie.split('=')
            if name in browser.cookies:
                del browser.cookies[name]
            browser.cookies.create(name, value.strip('"'), path='/')
    return browser
