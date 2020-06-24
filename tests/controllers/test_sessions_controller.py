#
# Tests for Sessions Controller
#


#
# [GET] /login
#
def test_get_login(api):
    r = api.requests.get("/login")
    assert r.status_code == 200


#
# [post] /login
#
def test_post_login(api, db_session):
    r = api.requests.post(
        "/login", {"email": "user1@example.com", "password": "password"}
    )
    assert r.status_code == 303
    assert r.cookies.get("session") is not None


# TODO: Add invalid case
def test_post_login_with_invalid_email(api, db_session):
    r = api.requests.post("/login", {"email": "missing_email", "password": "password"})
    assert r.status_code == 422
    assert r.cookies.get("session") is None


def test_post_login_with_without_params(api, db_session):
    r = api.requests.post("/login", {"email": "missing_email"})
    assert r.status_code == 422
    assert r.cookies.get("session") is None

    r = api.requests.post("/login", {"password": "password"})
    assert r.status_code == 422
    assert r.cookies.get("session") is None


def test_post_login_with_missing_email(api, db_session):
    r = api.requests.post(
        "/login", {"email": "missing_email@test.com", "password": "password"}
    )
    assert r.status_code == 403
    assert r.cookies.get("session") is None


def test_post_login_with_missing_password(api, db_session):
    r = api.requests.post(
        "/login", {"email": "user1@example.com", "password": "invalid-password"}
    )
    assert r.status_code == 403
    assert r.cookies.get("session") is None


#
# [POST] /logout
#
def test_post_logout(api):
    # login
    r = api.requests.post(
        "/login", {"email": "user1@example.com", "password": "password"}
    )
    assert r.cookies.get("session") is not None

    # logout
    r = api.requests.post("/logout")
    assert r.status_code == 303
    assert r.cookies.get("session") is None


def test_post_logout_when_not_logged_in(api):
    r = api.requests.post("/logout")
    assert r.status_code == 303
    assert r.cookies.get("session") is None
