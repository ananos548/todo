from pydantic import BaseModel, ConfigDict
from enum import Enum


class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    status: TaskStatusEnum


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: TaskStatusEnum = None


class TaskCreate(BaseModel):
    title: str
    description: str = None
    status: TaskStatusEnum = TaskStatusEnum.pending
