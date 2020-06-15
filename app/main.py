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

# deprecated
def get_db_session():
    return app.db_helper.session()

api = responder.API(
    templates_dir = "app/templates"
)

@api.route("/")
def root_path(req, resp):
    resp.html = api.template('index.html')

@api.route("/hello/{who}")
def hello_to(req, resp, *, who):
    resp.text = f"Hello, {who}! how are you?"

@api.route("/hello/{who}/html")
def hello_html(req, resp, *, who):
    resp.html = api.template('hello.html', who=who)

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

#
# DB connection test
#
@api.route("/user/{idx}/update")
def user_update(req, resp, *, idx):
    if idx == None:
        resp.text = "ERROR: you must specify id"
        return
    else:
        idx = int(idx)

    session = get_db_session()
    user = session.query(User).get(idx)
    if user == None:
        resp.text = f"User not found ({idx})."
    else:
        user.name = req.params.get('name', user.name)
        user.profile = req.params.get('profile', user.profile)
        user.location = req.params.get('location', user.location)
        session.commit()
        resp.text = f"User Update: {user}"

@api.route("/user/{idx}/delete")
def user_delete(req, resp, *, idx):
    if idx == None:
        resp.text = "ERROR: you must specify id"
        return
    else:
        idx = int(idx)

    session = get_db_session()
    user = session.query(User).get(idx)
    if user == None:
        resp.text = f"User not found ({idx})."
    else:
        session.delete(user)
        session.commit()
        resp.text = f"User Deleted: {idx}"

from app.controllers.users_controller import UsersController
api.add_route("/users", UsersController)

if __name__ == '__main__':
    api.run()

