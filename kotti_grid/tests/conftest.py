from pytest import fixture

pytest_plugins = "kotti"


@fixture
def kg_populate(db_session):
    from kotti_grid.populate import populate
    populate()
