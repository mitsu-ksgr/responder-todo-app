#
# Tests for Todos Controller
#
from datetime import datetime, timedelta

from app.helpers import db_helper
from app.models.todo import Todo, TodoStatus


# api.add_route("/todo/new", NewTodoController)
# api.add_route("/todo/{idx}", TodoController)

#
# [GET] /todolist
#
def test_get_todolist(api, current_user):
    r = api.requests.get("/todolist")
    assert r.status_code == 200


def test_get_todolist_not_loggin(api):
    r = api.requests.get("/todolist")
    assert r.status_code == 401


#
# [GET] /todo/new
#
def test_get_todo_new(api, current_user):
    r = api.requests.get("/todo/new")
    assert r.status_code == 200


def test_get_todo_new_not_loggin(api):
    r = api.requests.get("/todo/new")
    assert r.status_code == 401


#
# [POST] /todo/new
#
def test_post_todo_new(api, db_session, current_user):
    due_date = datetime.now() + timedelta(days=5)
    params = {
        "title": "Todo App",
        "due_date": due_date.date(),
        "description": "todo description",
    }
    r = api.requests.post("/todo/new", params)
    assert r.status_code == 201

    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    assert todo.title == params["title"]
    assert str(todo.due_date.date()) == str(due_date.date())
    assert todo.description == params["description"]
    assert todo.status == TodoStatus.none


def test_post_todo_new_no_loggin(api, db_session):
    r = api.requests.post("/todo/new", {})
    assert r.status_code == 401


def test_post_todo_new_invalid_params(api, db_session, current_user):
    r = api.requests.post(
        "/todo/new", {"title": None, "due_date": None, "description": None}
    )
    assert r.status_code == 422


#
# [GET] /todo/{idx}
#
def test_get_todo(api, db_session, current_user):
    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    r = api.requests.get(f"/todo/{todo.id}")
    assert r.status_code == 200


def test_get_todo_no_loggin(api):
    r = api.requests.get("/todo/1")
    assert r.status_code == 401


def test_get_todo_nonexistent_todo(api, current_user):
    r = api.requests.get("/todo/9999")
    assert r.status_code == 404


#
# [PATCH] /todo/{id}
#
def test_patch_todo(api, db_session, current_user):
    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    url = f"/todo/{todo.id}"

    due_date = datetime.now() + timedelta(days=7)
    changed = {
        "title": todo.title + " changed",
        "description": todo.description + " changed",
        "due_date": due_date.date(),
        "status": TodoStatus.wip.value,
    }
    r = api.requests.post(url, dict({"_method": "patch"}, **changed))
    assert r.status_code == 200

    session = db_helper.session()
    todo = session.query(Todo).get(todo.id)
    assert todo.title == changed["title"]
    assert todo.description == changed["description"]
    assert todo.due_date.date() == changed["due_date"]
    assert todo.status.value == changed["status"]


def test_patch_todo_no_loggin(api, db_session):
    r = api.requests.post("/user/1", {"_method": "patch", "name": "changed"})
    assert r.status_code == 401


def test_patch_todo_with_invalid_params(api, db_session, current_user):
    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    url = f"/todo/{todo.id}"

    due_date = datetime.now() - timedelta(days=7)
    r = api.requests.post(url, {"_method": "patch", "due_date": due_date.date()})
    assert r.status_code == 422

    r = api.requests.post(url, {"_method": "patch", "status": "hoge"})
    assert r.status_code == 422


#
# [DELETE] /user/{id}
#
def test_delete_todo(api, db_session, current_user):
    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    r = api.requests.post(f"/todo/{todo.id}", {"_method": "delete"})
    assert r.status_code == 201

    session = db_helper.session()
    todo = session.query(Todo).get(todo.id)
    assert todo is None


def test_delete_user_no_loggin(api, db_session, current_user):
    todo = (
        db_session.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .order_by(Todo.id.desc())
        .first()
    )
    r = api.requests.post(f"/todo/{todo.id}", {"_method": "delete"})
    assert r.status_code == 403


def test_delete_user_delete_others_todo(api, db_session, current_user):
    r = api.requests.post("/todo/1", {"_method": "delete"})
    assert r.status_code == 403
