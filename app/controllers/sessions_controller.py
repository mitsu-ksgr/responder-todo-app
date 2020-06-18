import bcrypt

import app.db_helper
from app.api_helper import redirect_to, render_template
from app.models.user import User


class LogoutController:
    async def on_get(self, req, resp):
        resp.session.pop("user_id")


        redirect_to(resp, "/")


class LoginController:
    async def on_get(self, req, resp):
        resp.html = render_template("sessions/new.html")

    async def on_post(self, req, resp):
        params = await req.media()
        valid, msg = self._validate(params)
        if not valid:
            resp.html = render_template("sessions/new.html", messages=msg)
            return

        is_auth, user = self._authenticate(params["email"], params["password"])
        if not is_auth:
            msg = ["Authentication failed."]
            resp.html = render_template("sessions/new.html", messages=msg)
            return

        # Login
        resp.session["user_id"] = user.id
        resp.html = render_template("sessions/new.html")

    def _validate(self, params):
        msg = []
        if "email" not in params:
            msg.append("Email can't be blank")
        if "password" not in params:
            msg.append("Password can't be blank")
        return len(msg) == 0, msg

    def _authenticate(self, email, row_password):
        session = app.db_helper.session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            check = bcrypt.checkpw(
                row_password.encode("utf-8"), user.encrypted_password.encode("utf-8")
            )
            if check:
                return True, user
        return False, None
