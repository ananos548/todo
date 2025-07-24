from fastapi import HTTPException
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.tasks_models import TaskStatus, Task
from src.schemas.tasks_schemas import TaskUpdate, TaskCreate

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_task(self, task: TaskCreate, user_id: int):
        new_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=user_id,
        )
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return new_task

    async def get_tasks(self, user_id: int, status: TaskStatus = None):
        stmt = select(Task).where(Task.user_id == user_id)
        if status:
            stmt = stmt.where(Task.status == status)
        results = await self.session.execute(stmt)
        return results.scalars().all()

    async def update_task(self, task_id: int, user_id: int, data: TaskUpdate):
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int):
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await self.session.delete(task)
        await self.session.commit()