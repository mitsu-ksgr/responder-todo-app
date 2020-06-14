#
# responder sample app
#
# see: https://responder.kennethreitz.org/en/latest/quickstart.html
#
import responder

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

#
# DB connection test
#
@api.route("/users/new")
def user_add(req, resp):
    import sqlalchemy
    import sqlalchemy.orm
    url = 'mysql+mysqlconnector://dev_user:password@db:3306/app'
    engine = sqlalchemy.create_engine(url, echo=False)

    # make session
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    from app.models import users

    name = req.params.get('name', 'test-user')
    profile = req.params.get('profile', 'profile text')

    user = users.User(name=name, profile=profile)
    session.add(user)
    session.commit()
    resp.text = "User Add: {}".format(user)

@api.route("/users")
def user_list(req, resp):
    import sqlalchemy
    import sqlalchemy.orm
    url = 'mysql+mysqlconnector://dev_user:password@db:3306/app'
    engine = sqlalchemy.create_engine(url, echo=False)

    # make session
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    from app.models import users

    text = ""
    for user in session.query(users.User).all():
        text += f"{user}\n"

    resp.text = text
    session.close()


if __name__ == '__main__':
    api.run()

