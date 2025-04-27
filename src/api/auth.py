from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.repos.r_users import UsersRepos
from src.schemas.schem_users import UsersRequestAdd, UsersAdd
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/register')
async def register_users(data: UsersRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            await UsersRepos(session).add(new_user_data)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail='Email address already in use. Please try a different address or '
                                                    'log in')
    return {'Status': 'OK'}
