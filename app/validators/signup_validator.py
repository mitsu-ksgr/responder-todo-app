from app.helpers import db_helper
from app.models.user import User
from app.validators.email_validator import EmailValidator


class SignupValidator:
    def __init__(self, params={}):
        self.valid = None
        self.messages = []
        self.is_valid(params)

    def is_valid(self, params):
        self.messages = []
        if "name" not in params:
            self.messages.append("Username can't be blank")
        if "email" not in params:
            self.messages.append("Email can't be blank")
        else:
            ev = EmailValidator(params["email"])
            if not ev.valid:
                self.messages += ev.messages
        if "password" not in params:
            self.messages.append("Password can't be blank")
        else:
            if len(params["password"]) < 6:
                self.messages.append("Password must be at least 6 characters")

        # check email uniqueness
        if "email" in params:
            session = db_helper.session()
            user = session.query(User).filter(User.email == params["email"]).first()
            if user is not None:
                self.messages.append("Email is invalid or already registered.")
            session.close()

        self.valid = len(self.messages) == 0
        return self.valid
