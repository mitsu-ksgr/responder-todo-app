#
# Todos Controller
#
#

# /todo_list/
#   - [GET]     ... user's todo list
#   - [POST]    ... create user's new todo
#

# /todo/{id}
#   [GET]       ... get todo details
#   [PATCH]     ... update todo
#   [DELETE]    ... delete todo


from sqlalchemy.exc import SQLAlchemyError

from app.helpers import db_helper
from app.helpers.api_helper import render_template, jinja2_template
from app.helpers.session_helper import current_user
from app.models.todo import Todo, TodoStatus
from app.validators.todo_validator import TodoValidator


def _render_todo_template(resp, template_name, **values):
    template = jinja2_template(resp, template_name)
    template.globals["TodoStatus"] = TodoStatus
    return template.render(**values)


# TODO: error handling

# /todolist
class TodoListController:
    # show user's todo
    async def on_get(self, req, resp):
        session = db_helper.session()
        me = current_user(resp, session)
        if me is None:
            resp.status_code = 401
            resp.html = render_template(resp, "401.html")
            session.close()
            return

        resp.html = _render_todo_template(resp, "todos/index.html", user=me)


# [GET]     /todo/new
# [POST]    /todo/new
class NewTodoController:
    async def on_get(self, req, resp):
        session = db_helper.session()
        me = current_user(resp, session)
        if me is None:
            resp.status_code = 401
            resp.html = render_template(resp, "401.html")
            session.close()
            return
        resp.html = _render_todo_template(resp, "todos/new.html", user=me)

    async def on_post(self, req, resp):
        session = db_helper.session()
        me = current_user(resp, session)
        if me is None:
            resp.status_code = 401
            resp.html = render_template(resp, "401.html")
            session.close()
            return

        params = await req.media()
        validator = TodoValidator(params)
        if not validator.valid:
            resp.status_code = 422
            resp.html = _render_todo_template(
                resp, "todos/new.html", messages=validator.messages
            )
            session.close()
            return

        err_msg = []
        try:
            todo = Todo(
                user_id=me.id,
                title=params["title"],
                status=TodoStatus.none,
                description=params.get("description", ""),
                due_date=params.get("due_date", None),
            )
            session.add(todo)
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            err_msg.append("Internal Server Error")
            session.rollback()
        except Exception as e:
            print(e)
            err_msg.append("Internal Server Error")
            session.rollback()
        finally:
            pass

        if len(err_msg) > 0:
            resp.status_code = 500
            resp.html = _render_todo_template(
                "todos/new.html", messages=validator.messages
            )
        else:
            resp.status_code = 201
            resp.html = _render_todo_template(resp, "todos/index.html", user=me)
        session.close()


# /todo/{id}
class TodoController:
    async def on_get(self, req, resp, *, idx):
        session = db_helper.session()
        me = current_user(resp, session)
        if me is None:
            resp.status_code = 401
            resp.html = render_template(resp, "401.html")
            session.close()
            return
        try:
            idx = int(idx)
            todo = session.query(Todo).get(idx)
        except ValueError:
            todo = None

        if todo:
            resp.status_code = 200
            resp.html = _render_todo_template(resp, "todos/show.html", user=me, todo=todo)
        else:
            resp.status_code = 404
            resp.html = render_template(resp, "404.html")

    async def on_post(self, req, resp, *, idx):
        session = db_helper.session()
        me = current_user(resp, session)
        if me is None:
            resp.status_code = 401
            resp.html = render_template(resp, "401.html")
            session.close()
            return

        try:
            idx = int(idx)
            todo = (
                session.query(Todo)
                .filter(Todo.user_id == me.id)
                .filter(Todo.id == idx)
                .first()
            )
        except ValueError:
            todo = None

        if todo is None:
            resp.status_code = 403
            resp.html = render_template(resp, "403.html")
            session.close()
            return

        params = await req.media()
        if "_method" in params:
            if params["_method"] == "patch":
                self.on_patch(req, resp, session, me, todo, params)
            elif params["_method"] == "delete":
                self.on_delete(req, resp, session, me, todo)

        session.close()

    def on_patch(self, req, resp, db_session, me, todo, params):
        validator = TodoValidator(params)
        if not validator.valid:
            resp.status_code = 422
            resp.html = _render_todo_template(
                resp, "todos/show.html", user=me, todo=todo, messages=validator.messages
            )
            db_session.close()
            return

        todo.title = params.get("title", todo.title)
        todo.status = TodoStatus.value_of(params.get("status", todo.status))
        todo.due_date = params.get("due_date", todo.due_date)
        todo.description = params.get("description", todo.description)

        has_err = False
        try:
            db_session.add(todo)
            db_session.commit()
        except SQLAlchemyError as e:
            print(e)
            db_session.rollback()
            has_err = True
        except Exception as e:
            print(e)
            db_session.rollback()
            has_err = True

        if has_err:
            resp.status_code = 500
            resp.html = render_template(resp, "500.html")
        else:
            resp.status_code = 200
            resp.html = _render_todo_template(
                resp, "todos/show.html", user=me, todo=todo, messages=validator.messages
            )
        db_session.close()

    def on_delete(self, req, resp, db_session, me, todo):
        ok = False
        try:
            db_session.delete(todo)
            db_session.commit()
            ok = True
        except SQLAlchemyError as e:
            print(e)
            db_session.rollback()
        except Exception as e:
            print(e)
            db_session.rollback()
        finally:
            pass

        if ok:
            resp.status_code = 201
            resp.html = _render_todo_template(resp, "todos/index.html", user=me)
        else:
            resp.status_code = 500
            resp.html = render_template(resp, "500.html")
        db_session.close()
