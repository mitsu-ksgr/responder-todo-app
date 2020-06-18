from app.helpers import db_helper
from app.helpers.api_helper import redirect_to, render_template
from app.helpers.session_helper import verify_password, login, logout
from app.models.user import User


class LogoutController:
    async def on_get(self, req, resp):
        logout(resp)
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
        login(resp, user.id)
        resp.html = render_template("sessions/new.html")

    def _validate(self, params):
        msg = []
        if "email" not in params:
            msg.append("Email can't be blank")
        if "password" not in params:
            msg.append("Password can't be blank")
        return len(msg) == 0, msg

    def _authenticate(self, email, row_password):
        session = db_helper.session()
        user = session.query(User).filter(User.email == email).first()
        if user and verify_password(row_password, user.encrypted_password):
            return True, user
        return False, None
