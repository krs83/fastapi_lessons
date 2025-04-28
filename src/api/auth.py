from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.repos.r_users import UsersRepos
from src.schemas.schem_users import UsersRequestAdd, UsersAdd
from src.database import async_session_maker

from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_users(data: UsersRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            await UsersRepos(session).add(new_user_data)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail='Email address already in use. Please try a different address or '
                                                    'log in')
    return {'Status': 'OK'}


@router.post('/login')
async def login_users(data: UsersRequestAdd,
                      response: Response):

    async with async_session_maker() as session:
        user = await UsersRepos(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='The user is not registered with such an e-mail')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Incorrect password')
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}
