#
# responder sample app
#
# see: https://responder.kennethreitz.org/en/latest/quickstart.html
#

import responder
import sqlalchemy
import sqlalchemy.orm

from config import app_config
from app.models import users

def get_db_session():
    url = app_config.get('db', 'url')
    engine = sqlalchemy.create_engine(url, echo=False)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()

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
@api.route("/users/new")
def user_add(req, resp):
    session = get_db_session()

    name = req.params.get('name', 'test-user')
    profile = req.params.get('profile', 'profile text')

    user = users.User(name=name, profile=profile)
    session.add(user)
    session.commit()
    resp.text = "User Add: {}".format(user)

@api.route("/user/{idx}/update")
def user_update(req, resp, *, idx):
    if idx == None:
        resp.text = "ERROR: you must specify id"
        return
    else:
        idx = int(idx)

    session = get_db_session()
    user = session.query(users.User).get(idx)
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
    user = session.query(users.User).get(idx)
    if user == None:
        resp.text = f"User not found ({idx})."
    else:
        session.delete(user)
        session.commit()
        resp.text = f"User Deleted: {idx}"

@api.route("/users")
def user_list(req, resp):
    session = get_db_session()
    text = ""
    for user in session.query(users.User).all():
        text += f"{user}\n"

    resp.text = text
    session.close()


if __name__ == '__main__':
    api.run()

