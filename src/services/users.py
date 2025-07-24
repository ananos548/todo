import jwt
from fastapi import Depends, HTTPException, Cookie
from starlette import status

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from src.database import get_async_session
from src.models.auth_models import User
from src.schemas.auth_schemas import UserSchemaAdd

SECRET_KEY = "SnSYSxw3Nq"
ALGORITHM = "HS256"

password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_user(self, user: UserSchemaAdd):
        new_user = User(username=user.username, email=user.email, hashed_password=password_hashing.hash(user.password))
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def authenticate(self, username: str, hashed_password: str):
        result = await self.session.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        if not password_hashing.verify(hashed_password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(username: str, user_id: int, expires_delta: timedelta = None):
        encode = {"sub": username, "id": user_id}
        expires = datetime.now() + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_current_user(cookie_jwt: str = Cookie(None)):
        if not cookie_jwt:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

        try:
            payload = jwt.decode(cookie_jwt, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            user_id = payload.get("id")
            return {"user_id": user_id, "username": username}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")