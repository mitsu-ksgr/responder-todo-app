from app.models.user import User


#
# UsersController
#
def test_users_get(api):
    r = api.requests.get("/users")
    assert r.status_code == 200


def test_users_post(api, db_session):
    email = "test3@example.com"
    r = api.requests.post(
        "/users", {"email": f"{email}", "password": "password", "name": "test user"}
    )
    assert r.status_code == 301

    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
