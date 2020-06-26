from faker import Faker

from app.helpers.session_helper import hash_password
from app.models.user import User


def generate_serial_users(n = 10):
    assert n >= 1
    users = []
    for i in range(1, n + 1):
        users.append(User(
            name = f"User{i}",
            email = f"user{i}@example.com",
            encrypted_password=hash_password("password"),
            location = f"city{i} Japan",
            profile = f"Hi, I'm user{i}!"
        ))
    return users


def generate_fake_users(n = 10):
    assert n >= 1
    fake = Faker()
    users = []
    for i in range(1, n + 1):
        users.append(User(
            name = fake.name(),
            email = fake.safe_email(),
            encrypted_password=hash_password("password"),
            location = f"{fake.city()} {fake.country()}",
            profile = fake.paragraph(),
        ))
    return users

