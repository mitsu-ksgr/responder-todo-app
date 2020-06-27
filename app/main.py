#
# responder sample app
#
# see: https://responder.kennethreitz.org/en/latest/quickstart.html
#

import os
import responder

from app.controllers.sessions_controller import LoginController, LogoutController
from app.controllers.signup_controller import SignupController
from app.controllers.users_controller import UsersController, UserController
from app.controllers.todos_controller import (
    TodoListController,
    NewTodoController,
    TodoController,
)
from config import app_config

# NOTE: in prod, you should set the RESPONDER_SECRET_KEY environment value./pp
api = responder.API(
    templates_dir="app/templates",
    secret_key=os.environ.get("RESPONDER_SECRET_KEY", "NOTASECRET"),
)


@api.route("/")
def root_path(req, resp):
    from app.helpers.api_helper import render_template

    resp.html = render_template(resp, "index.html")


# Sessions
api.add_route("/join", SignupController)
api.add_route("/login", LoginController)
api.add_route("/logout", LogoutController)

# Users
api.add_route("/users", UsersController)
api.add_route("/user/{idx}", UserController)

# Todo
api.add_route("/todolist", TodoListController)
api.add_route("/todo/new", NewTodoController)
api.add_route("/todo/{idx}", TodoController)

# Debug
if app_config.env == "development":
    from app.controllers.debug_controller import DebugController

    api.add_route("/debug", DebugController)

if __name__ == "__main__":
    api.run()
