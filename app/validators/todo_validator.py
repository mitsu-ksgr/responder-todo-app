from datetime import date, datetime

from app.models.todo import TodoStatus


class TodoValidator:
    def __init__(self, params={}):
        self.valid = None
        self.messages = []
        self.is_valid(params)

    def is_valid(self, params):
        self.messages = []
        if "title" not in params:
            self.messages.append("Title can't be blank")
        if "due_date" in params:
            due_date = datetime.strptime(params["due_date"], "%Y-%m-%d")
            today = datetime.combine(date.today(), datetime.min.time())
            if due_date < today:
                self.messages.append("The due date is in the past")

        if "status" in params:
            if not TodoStatus.is_value(params["status"]):
                self.messages.append("Invalid status")

        self.valid = len(self.messages) == 0
        return self.valid
