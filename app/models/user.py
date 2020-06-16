#!/usr/bin/python

from datetime import datetime

from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp


class User(declarative_base()):
    __tablename__ = "users"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(50))
    profile = Column(String(200, convert_unicode=True))
    location = Column(String(128, convert_unicode=True))
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
        return "<User(id={}, name='{}', location={}, created_at='{}', updated_at='{}')>".format(
            self.id, self.name, self.location, self.created_at, self.updated_at
        )
