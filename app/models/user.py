import datetime
import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=uuid.uuid4())
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    email_verified_at = Column(TIMESTAMP, nullable=True)
    password = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    status = Column(String, nullable=True, default="active")
    is_deleted = Column(Integer, default=False)
    remember_token = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.datetime.now())