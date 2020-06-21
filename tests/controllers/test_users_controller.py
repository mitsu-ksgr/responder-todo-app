#
# Tests for Users Controller
#


#
# [GET] /users
#
def test_get_users(api):
    r = api.requests.get("/users")
    assert r.status_code == 200
