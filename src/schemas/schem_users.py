from pydantic import BaseModel, ConfigDict, EmailStr


class UsersRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UsersAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class Users(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
