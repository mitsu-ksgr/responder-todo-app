from sqlalchemy.exc import SQLAlchemyError

from app.helpers import db_helper
from app.helpers.api_helper import redirect_to, render_template
from app.helpers.session_helper import hash_password
from app.models.user import User
from app.validators.user_validator import UserValidator


# TODO: error handling

# /users
class UsersController:
    # shows all users
    async def on_get(self, req, resp):
        session = db_helper.session()
        users = session.query(User).all()
        resp.html = render_template("users/index.html", users=users)


# /user/{idx}
class UserController:
    async def on_get(self, req, resp, *, idx):
        if idx is None:
            redirect_to(resp, "/users")
            return
        else:
            idx = int(idx)

        session = db_helper.session()
        user = session.query(User).get(idx)
        resp.html = render_template("users/show.html", user=user)

    async def on_post(self, req, resp, *, idx):
        if idx is None:
            redirect_to(resp, "/users")
            return
        else:
            idx = int(idx)

        params = await req.media()
        if "_method" in params:
            if params["_method"] == "patch":
                self.on_patch(req, resp, idx, params)
                return
            elif params["_method"] == "delete":
                self.on_delete(req, resp, idx)
                return

        # invalid request error
        # TODO: with flash message?
        redirect_to(resp, f"/user/{idx}")
        return

    def on_patch(self, req, resp, idx, params):
        session = db_helper.session()
        user = session.query(User).get(idx)
        if not user:
            # Note: users/show.html allows none user
            resp.html = render_template("users/show.html", user=user)
            session.close()
            return

        # TODO: check email uniqueness
        validator = UserValidator("update", params)
        if not validator.valid:
            resp.html = render_template(
                "users/show.html", user=user, messages=validator.messages
            )
            return

        user.email = params.get("email", user.email)
        user.name = params.get("name", user.name)
        user.profile = params.get("profile", user.profile)
        user.location = params.get("location", user.location)
        if "password" in params:
            user.encrypted_password = hash_password(params["password"])

        try:
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
        except Exception as e:
            print(e)
            session.rollback()
        resp.html = render_template("users/show.html", user=user)
        session.close()

    def on_delete(self, req, resp, idx):
        session = db_helper.session()
        user = session.query(User).get(idx)
        if not user:
            redirect_to(resp, "/users")
            session.close()
            return
        try:
            session.delete(user)
            session.commit()
            redirect_to(resp, "/users")
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            resp.html = render_template("users/show.html", user=user)
        except Exception as e:
            print(e)
            session.rollback()
            resp.html = render_template("users/show.html", user=user)
        finally:
            session.close()
