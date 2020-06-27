import pytest

import app.main
from app.helpers import db_helper


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
    from db.dummy.todos import add_serial_todos_to_user

    session = db_helper.session()
    users = generate_serial_users(10)
    for user in users[:5]:
        add_serial_todos_to_user(user)
    session.add_all(users)
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
    # clear session/cookies for each tests
    api = app.main.api
    s = api.session()
    s.cookies.clear()

    return api


@pytest.fixture
def db_session():
    return db_helper.session()


@pytest.fixture
def current_user():
    from faker import Faker

    from app.helpers.session_helper import hash_password
    from app.models.user import User
    from app.models.todo import Todo

    fake = Faker()
    email = f"test_user_{fake.random_number(digits=10)}@test.com"
    user = User(
        name=fake.name(),
        email=email,
        encrypted_password=hash_password("password"),
        location=f"{fake.city()} {fake.country()}",
        profile=fake.paragraph(),
    )
    user.todos.append(Todo(title="Test Todo", status="none", description="test todo",))

    session = db_helper.session()
    session.add(user)
    session.commit()
    user = session.query(User).filter(User.email == email).first()
    session.close()

    api = app.main.api
    api.requests.post("/login", {"email": user.email, "password": "password"})

    return user
