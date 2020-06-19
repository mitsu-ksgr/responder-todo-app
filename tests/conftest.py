import pytest


@pytest.fixture
def api():
    import app.main

    return app.main.api


@pytest.fixture
def db_session():
    import app.helpers.db_helper

    return app.helpers.db_helper.session()
