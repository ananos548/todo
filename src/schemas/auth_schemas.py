from pydantic import BaseModel


class UserSchemaAdd(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str