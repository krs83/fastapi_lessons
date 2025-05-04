from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel

from fastapi import Request, HTTPException

from src.db_manager import DBManager
from src.services.auth import AuthService
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=3, ge=1, lt=5)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='There is no any access_token provided')
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_dp():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_dp)]
