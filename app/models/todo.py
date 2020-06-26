import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql.functions import current_timestamp

from app.models.base import Base


class TodoStatus(enum.Enum):
    none = 0
    wip = 1
    pending = 2
    done = 3


class Todo(Base):
    __tablename__ = "todos"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("users.id"))
    title = Column(String(255))
    status = Column(Enum(TodoStatus))
    description = Column(Text)
    due_date = Column(DateTime)
    created_at = Column(
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    updated_at = Column(
        DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now()
    )

    def __repr__(self):
        return (
            "<Todo("
            "id={}, user_id={}, title='{}', status={}, "
            "created_at={}, updated_at={}"
            ")>"
        ).format(
            self.id,
            self.user_id,
            self.title,
            self.status,
            self.created_at,
            self.updated_at,
        )
