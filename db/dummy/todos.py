from datetime import datetime, timedelta
import random

from faker import Faker

from app.helpers.session_helper import hash_password
from app.models.todo import Todo, TodoStatus


def _random_status():
    return random.choice(list(TodoStatus))


def _random_due_date():
    gen_funcs = {
        "none": lambda: None,
        "future": lambda: datetime.now() + timedelta(days=random.randint(1, 30)),
        "past": lambda: datetime.now() - timedelta(days=random.randint(1, 30)),
    }
    return gen_funcs[random.choice(list(gen_funcs))]()


def add_serial_todos_to_user(user, n = 10):
    assert n >= 1
    for i in range(1, n + 1):
        due = datetime.now() + timedelta(days=i)
        user.todos.append(Todo(
            title = f"Task {i}",
            status = TodoStatus.none,
            description = f"task {i}, by {due}!",
            due_date = due
        ))


def add_dummy_todos_to_user(user, n = 10):
    assert n >= 1
    fake = Faker()
    for i in range(1, n + 1):
        due = datetime.now() + timedelta(days=i)
        user.todos.append(Todo(
            title = fake.sentence(),
            status = _random_status(),
            description = fake.text(),
            due_date = _random_due_date(),
        ))



