from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class BaseModel(object):

    __id = Column(UUID, default=uuid4(), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)

    def get_id(self):
        return self.__id
