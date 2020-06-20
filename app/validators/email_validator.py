import re

_regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")


class EmailValidator:
    def __init__(self, email):
        self.valid = None
        self.messages = []
        self.is_valid(email)

    def is_valid(self, email):
        self.messages = []
        if email is None or len(email) == 0:
            self.messages.append("Email can't be blacnk")
        elif not _regex.match(email):
            self.messages.append("Email is invalid")

        self.valid = len(self.messages) == 0
        return self.valid
