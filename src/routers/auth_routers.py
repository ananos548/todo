from datetime import timedelta
from starlette import status
from fastapi import APIRouter, Depends, Cookie, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.schemas.auth_schemas import UserSchemaAdd
from src.services.users import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],

)


@router.post("/registration")
async def create_user(
        new_user: UserSchemaAdd,
        service: UserService = Depends(UserService)
):
    user = await service.add_user(new_user)
    return {"user_id": user.id}


@router.post("/login")
async def login_for_access_token(
        service: UserService = Depends(UserService),
        form_data: OAuth2PasswordRequestForm = Depends(),
        cookie_jwt: str = Cookie(None)):
    if cookie_jwt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already authenticated")

    user = await service.authenticate(form_data.username, form_data.password)
    token = service.create_access_token(user_id=user.id, username=user.username,
                                        expires_delta=timedelta(minutes=360000))
    response = JSONResponse(content={"message": "successfully"})
    response.set_cookie(
        key="cookie_jwt",
        value=token
    )
    return response


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("cookie_jwt")
    return {"message": "Logged out successfully"}


@router.get("/current_user")
async def get_current_user(cookie_jwt: str | None = Cookie(default=None), service: UserService = Depends(UserService)):
    user_data = service.get_current_user(cookie_jwt)
    return user_data