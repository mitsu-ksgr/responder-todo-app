#
# Tests for Users Controller
#
from app.models.user import User


#
# [GET] /users
#
def test_get_users(api):
    r = api.requests.get("/users")
    assert r.status_code == 200
    # TODO: check contain users


#
# [GET] /user/{id}
#
def test_get_user(api):
    r = api.requests.get("/user/1")
    assert r.status_code == 200


def test_get_user_nonexistent_user(api):
    r = api.requests.get("/user/9999")
    assert r.status_code == 404

    r = api.requests.get("/user/abcd")
    assert r.status_code == 404


#
# [PATCH] /user/{id}
#
def test_patch_user(api, db_session, current_user):
    url = f"/user/{current_user.id}"
    changed = {
        "name": current_user.name + "-changed",
        "location": current_user.location + "-changed",
        "profile": current_user.profile + "-changed",
    }
    r = api.requests.post(url, dict({"_method": "patch"}, **changed))
    assert r.status_code == 200

    user = db_session.query(User).get(current_user.id)
    assert user.name == changed["name"]
    assert user.location == changed["location"]
    assert user.profile == changed["profile"]


def test_patch_user_no_loggin(api, db_session):
    r = api.requests.post("/user/1", {"_method": "patch", "name": "changed"})
    assert r.status_code == 401


def test_patch_user_update_others(api, db_session, current_user):
    r = api.requests.post("/user/1", {"_method": "patch", "name": "changed"})
    assert r.status_code == 403


def test_patch_user_with_invalid_params(api, db_session, current_user):
    url = f"/user/{current_user.id}"
    r = api.requests.post(url, {"_method": "patch", "password": "123"})
    assert r.status_code == 422


#
# [DELETE] /user/{id}
#
def test_delete_user(api, db_session, current_user):
    r = api.requests.post(f"/user/{current_user.id}", {"_method": "delete"})
    assert r.status_code == 200

    user = db_session.query(User).get(current_user.id)
    assert user is None


def test_delete_user_no_loggin(api, db_session):
    r = api.requests.post("/user/1", {"_method": "delete"})
    assert r.status_code == 401


def test_delete_user_delete_others(api, db_session, current_user):
    r = api.requests.post("/user/1", {"_method": "delete"})
    assert r.status_code == 403
