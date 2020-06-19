import pytest

import app.main as service


@pytest.fixture
def api():
    return service.api


def test_root_path(api):
    r = api.requests.get("/")
    assert r.status_code == 200


def test_db_info(api):
    r = api.requests.get("/db_info")
    assert r.status_code == 200
