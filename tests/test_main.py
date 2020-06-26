def test_root_path(api):
    r = api.requests.get("/")
    assert r.status_code == 200
