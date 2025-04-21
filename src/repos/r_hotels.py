from src.models.m_hotels import HotelsOrm
from src.repos.base import BaseRepos
from sqlalchemy import select, func


class HotelsRepos(BaseRepos):
    model = HotelsOrm

    async def get_all(self,
                      location,
                      title,
                      offset,
                      limit):

        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
