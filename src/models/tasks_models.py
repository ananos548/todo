from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey
from enum import Enum as Enumerate

from src.database import Base
from src.models.auth_models import User

class TaskStatus(Enumerate):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id))