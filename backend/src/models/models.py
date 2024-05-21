from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey

from datetime import datetime

Base = declarative_base()


class Mixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Test(Mixin, Base):
    __tablename__ = 'test'
    name = Column(String, nullable=False)


class Users(Base, Mixin):
    __tablename__ = "users"

    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)


class Token(Base, Mixin):
    __tablename__ = 'token'

    user_id = Column(Integer, ForeignKey('users.id'))

    token = Column(String, nullable=False, unique=True)
    expiration_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
