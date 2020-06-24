import pytest
import app.helpers.db_helper


#
# Database initializers
#
def _init_test_db():
    import alembic.config
    import sqlalchemy

    from config import app_config

    # cleanup db
    engine = sqlalchemy.create_engine(app_config.get("db", "url"), echo=False)
    results = engine.execute("SHOW TABLES")
    for result in results:
        table = result[0]
        engine.execute(f"DROP TABLE IF EXISTS {table}")

    # migrate to head
    argv = [
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=argv)


def _make_dummy_data():
    from db.dummy.users import generate_serial_users

    session = app.helpers.db_helper.session()
    session.bulk_save_objects(generate_serial_users())
    session.commit()


#
# Hooks
# see: https://stackoverflow.com/a/35394239
#
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    _init_test_db()
    _make_dummy_data()


#
# Fixtures
#
@pytest.fixture
def api():
    import app.main

    # clear session/cookies for each tests
    api = app.main.api
    s = api.session()
    s.cookies.clear()

    return api


@pytest.fixture
def db_session():
    import app.helpers.db_helper

    return app.helpers.db_helper.session()
