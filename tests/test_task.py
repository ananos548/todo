import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from datetime import timedelta, datetime
from main import app
from src.services.users import UserService, SECRET_KEY, ALGORITHM
from src.schemas.tasks_schemas import TaskCreate
import jwt

def get_test_token():
    payload = {
        "sub": "testuser",
        "id": 1,
        "exp": datetime.now() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@pytest.mark.asyncio
async def test_add_task():
    token = get_test_token()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/tasks",
            json={
                "title": "Test Task",
                "description": "Test description",
                "status": "pending",
            },
            cookies={"cookie_jwt": token}
        )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_get_tasks():
    token = get_test_token()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/tasks",
            cookies={"cookie_jwt": token}
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)