class UserValidator:
    def __init__(self, params):
        self.is_valid = None
        self.messages = []
        self.validate(params)

    def validate(self, params):
        self.messages = []
        if "name" not in params:
            self.messages.append("Name can't be blank")
        if "email" not in params:
            self.messages.append("Email can't be blank")
        if "password" not in params:
            self.messages.append("Password can't be blank")
        else:
            if len(params["password"]) < 6:
                self.messages.append("Password must be at least 6 characters")

        self.is_valid = len(self.messages) == 0
        return self.is_valid, self.messages

