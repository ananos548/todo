from fastapi import APIRouter, Depends, Query
from typing import Optional

from src.routers.dependencies import get_task_service
from src.schemas.tasks_schemas import TaskStatusEnum, TaskCreate, TaskUpdate
from src.services.tasks import TaskService
from src.services.users import UserService

router = APIRouter()


@router.post("/tasks")
async def create_task(
        task: TaskCreate,
        user_data: dict = Depends(UserService.get_current_user),
        service: TaskService = Depends(get_task_service),
):
    """ Создание задачи """
    user_id = user_data["user_id"]
    return await service.add_task(task, user_id)


@router.get("/tasks")
async def get_tasks(
        status: Optional[TaskStatusEnum] = Query(None),
        user_data: dict = Depends(UserService.get_current_user),
        service: TaskService = Depends(get_task_service)
):
    """ Получение задач (Есть возможность фильтровать по status) """
    return await service.get_tasks(user_id=user_data["user_id"], status=status)


@router.put("/tasks/{task_id}")
async def update_task(task_id: int,
                      task: TaskUpdate,
                      user_data: dict = Depends(UserService.get_current_user),
                      service: TaskService = Depends(get_task_service)):
    """ Изменить задачу """
    return await service.update_task(task_id, user_data["user_id"], task)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int,
                      user_data: dict = Depends(UserService.get_current_user),
                      service: TaskService = Depends(get_task_service)):
    """ Удалить задачу """
    return await service.delete_task(task_id, user_data["user_id"])