from pydantic import BaseModel, ConfigDict


class UsersRequestAdd(BaseModel):
    email: str
    password: str


class UsersAdd(BaseModel):
    email: str
    hashed_password: str


class Users(BaseModel):
    id: str
    email: str

    model_config = ConfigDict(from_attributes=True)
