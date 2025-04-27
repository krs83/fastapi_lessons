from fastapi import APIRouter

from src.repos.r_users import UsersRepos
from src.schemas.schem_users import UsersRequestAdd, UsersAdd
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_users(data: UsersRequestAdd):
    hashed_password = 'fadsf&^DSFDSFIJH'
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepos(session).add(new_user_data)

    return {'status': 'OK'}
