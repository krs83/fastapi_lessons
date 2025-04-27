from src.models.m_users import UsersOrm
from src.repos.base import BaseRepos
from src.schemas.schem_users import Users


class UsersRepos(BaseRepos):
    model = UsersOrm
    schema = Users
