from src.models.m_rooms import RoomsOrm
from src.repos.base import BaseRepos


class RoomsRepos(BaseRepos):
    model = RoomsOrm
