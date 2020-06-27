from sqlalchemy.exc import SQLAlchemyError

from app.helpers import db_helper
from app.helpers.api_helper import render_template
from app.helpers.session_helper import hash_password, current_user, logout
from app.models.user import User
from app.validators.user_validator import UserValidator


# TODO: error handling

# /users
class UsersController:
    # shows all users
    async def on_get(self, req, resp):
        session = db_helper.session()
        users = session.query(User).all()
        resp.status_code = 200
        resp.html = render_template(resp, "users/index.html", users=users)


# /user/{idx}
class UserController:
    async def on_get(self, req, resp, *, idx):
        session = db_helper.session()

        try:
            idx = int(idx)
            user = session.query(User).get(idx)
        except ValueError:
            user = None

        me = current_user(resp, session)
        if user:
            resp.status_code = 200
            resp.html = render_template(resp, "users/show.html", user=user, me=me)
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
            user = session.query(User).get(idx)
        except ValueError:
            user = None

        if user is None or me.id != user.id:
            resp.status_code = 403
            resp.html = render_template(resp, "403.html")
            session.close()
            return

        params = await req.media()
        if "_method" in params:
            if params["_method"] == "patch":
                self.on_patch(req, resp, session, me, user, params)
            elif params["_method"] == "delete":
                self.on_delete(req, resp, session, user)
        session.close()

    def on_patch(self, req, resp, db_session, me, user, params):
        validator = UserValidator("update", params)
        if not validator.valid:
            resp.status_code = 422
            resp.html = render_template(
                resp, "users/show.html", user=user, me=me, messages=validator.messages
            )
            return

        user.name = params.get("name", user.name)
        user.profile = params.get("profile", user.profile)
        user.location = params.get("location", user.location)
        if "password" in params:
            user.encrypted_password = hash_password(params["password"])

        has_err = False
        try:
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
            resp.html = render_template(resp, "users/show.html", user=user, me=user)

    def on_delete(self, req, resp, db_session, user):
        ok = False
        try:
            db_session.delete(user)
            db_session.commit()
            logout(resp)
            ok = True
        except SQLAlchemyError as e:
            print(e)
            db_session.rollback()
        except Exception as e:
            print(e)
            db_session.rollback()
        finally:
            db_session.close()

        if ok:
            resp.status_code = 200
            resp.html = render_template(resp, "users/deleted.html")
        else:
            resp.status_code = 500
            resp.html = render_template(resp, "500.html")
