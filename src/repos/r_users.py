from sqlalchemy import select

from src.models.m_users import UsersOrm
from src.repos.base import BaseRepos
from src.schemas.schem_users import Users, UsersWithHashedPassword
from pydantic import EmailStr


class UsersRepos(BaseRepos):
    model = UsersOrm
    schema = Users

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UsersWithHashedPassword.model_validate(model)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
