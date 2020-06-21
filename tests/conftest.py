import pytest


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


#
# Fixtures
#
@pytest.fixture
def api():
    import app.main

    return app.main.api


@pytest.fixture
def db_session():
    import sqlalchemy
    from config import app_config

    engine = sqlalchemy.create_engine(app_config.get("db", "url"), echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()
