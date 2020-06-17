# TODO: validate email format
class UserValidator:
    def __init__(self, context = None, params = {}):
        self.valid = None
        self.messages = []
        if context:
            self.is_valid(context, params)

    def is_valid(self, context, params):
        if context == 'create':
            self._validate_create_params(params)
        elif context == 'update':
            self._validate_update_params(params)
        return self.valid

    def _validate_create_params(self, params):
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
        self.valid = len(self.messages) == 0

    def _validate_update_params(self, params):
        self.messages = []
        if "name" in params and len(params["name"]) == 0:
            self.messages.append("Name can't be blank")
        if "email" in params and len(params["email"]) == 0:
            self.messages.append("Email can't be blank")
        if "password" in params and len(params["password"]) < 6:
            self.messages.append("Password must be at least 6 characters")
        self.valid = len(self.messages) == 0

