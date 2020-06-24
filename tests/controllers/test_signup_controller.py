#
# Tests for Signup Controller
#
from app.models.user import User


#
# [GET] /joins
#
def test_signup_get(api):
    r = api.requests.get("/join")
    assert r.status_code == 200


#
# [post] /joins
#
def test_signup_post(api, db_session):
    email = "post_joins_new_user@example.com"
    params = {
        "name": "new test user",
        "email": email,
        "password": "password",
    }
    r = api.requests.post("/join", params)
    assert r.status_code == 201
    assert r.cookies.get("session") is not None

    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None


def test_signup_post_without_email(api, db_session):
    params = {
        "name": "new test user",
        "password": "password",
    }
    r = api.requests.post("/join", params)
    assert r.status_code == 422


def test_signup_post_without_name(api, db_session):
    email = "post_joins_new_user_without_name@example.com"
    params = {
        "email": email,
        "password": "password",
    }
    r = api.requests.post("/join", params)
    assert r.status_code == 422

    user = db_session.query(User).filter(User.email == email).first()
    assert user is None


def test_signup_post_without_password(api, db_session):
    email = "post_joins_new_user_without_password@example.com"
    params = {
        "name": "new test user",
        "email": email,
    }
    r = api.requests.post("/join", params)
    assert r.status_code == 422

    user = db_session.query(User).filter(User.email == email).first()
    assert user is None


def test_signup_post_with_too_short_password(api, db_session):
    email = "post_joins_new_user_with_too_short_password@example.com"
    params = {
        "name": "new test user",
        "email": email,
        "password": "passw",
    }
    r = api.requests.post("/join", params)
    assert r.status_code == 422

    user = db_session.query(User).filter(User.email == email).first()
    assert user is None
