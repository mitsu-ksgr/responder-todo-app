from sqlalchemy.exc import SQLAlchemyError

from app.helpers import db_helper
from app.helpers.api_helper import render_template
from app.helpers.session_helper import hash_password
from app.models.user import User
from app.validators.signup_validator import SignupValidator


class SignupController:
    async def on_get(self, req, resp):
        resp.html = render_template("signup/join.html")

    async def on_post(self, req, resp):
        params = await req.media()
        validator = SignupValidator(params)
        if not validator.valid:
            resp.status_code = 422
            resp.html = render_template("signup/join.html", messages=validator.messages)
            return

        session = db_helper.session()
        err_msg = []
        try:
            hashed_pass = hash_password(params["password"])
            user = User(
                name=params["name"],
                email=params["email"],
                encrypted_password=hashed_pass,
            )
            session.add(user)
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
            session.close()

        if len(err_msg) > 0:
            resp.status_code = 500
            resp.html = render_template("signup/join.html", messages=err_msg)
        else:
            resp.status_code = 201
            resp.html = render_template("signup/registered.html")
