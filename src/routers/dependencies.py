from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.services.tasks import TaskService
from src.services.users import UserService


def get_task_service(
    session: AsyncSession = Depends(get_async_session),
) -> TaskService:
    return TaskService(session)

def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)