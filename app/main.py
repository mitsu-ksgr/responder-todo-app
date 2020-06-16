#
# responder sample app
#
# see: https://responder.kennethreitz.org/en/latest/quickstart.html
#

import responder
import sqlalchemy
import sqlalchemy.orm

from config import app_config
from app.models.user import User

import app.db_helper

api = responder.API(templates_dir="app/templates")


@api.route("/")
def root_path(req, resp):
    resp.html = api.template("index.html")


@api.route("/db_info")
def db_info(req, resp):
    txt = ""
    txt += f"Dialect: {app_config.get('db', 'dialect')}\n"
    txt += f"Driver: {app_config.get('db', 'driver')}\n"
    txt += f"Host: {app_config.get('db', 'host')}\n"
    txt += f"Port: {app_config.get('db', 'port')}\n"
    txt += f"User Name: {app_config.get('db', 'username')}\n"
    txt += f"URL: {app_config.get('db', 'url')}\n"
    resp.text = txt


from app.controllers.users_controller import UsersController, UserController

api.add_route("/users", UsersController)
api.add_route("/user/{idx}", UserController)

if __name__ == "__main__":
    api.run()
