from src.models.m_hotels import HotelsOrm
from src.repos.base import BaseRepos


class HotelsRepos(BaseRepos):
    model = HotelsOrm
