from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from app.models.base import Base
from app.models.todo import Todo  # noqa: F401 ... for init sqlalchemy's mapper


class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    email = Column(String(255))
    encrypted_password = Column(String(255))
    name = Column(String(255))
    location = Column(String(255))
    profile = Column(Text)
    created_at = Column(
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    updated_at = Column(
        DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now()
    )

    # Relations
    todos = relationship("Todo", backref="user.id")

    def __repr__(self):
        return "<User(id={}, name='{}', created_at={}, updated_at={})>".format(
            self.id, self.name, self.created_at, self.updated_at
        )
