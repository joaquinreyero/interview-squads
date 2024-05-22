from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime, Boolean, Text

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

class BlogPost(Base, Mixin):
    __tablename__ = 'blog_post'

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    transcription = Column(Text, nullable=False)
