from sqlalchemy import select


class BaseRepos:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **by_filters):
        query = select(self.model)
        result = await self.session.execute(query).filter_by(by_filters)
        return result.scalars().one_or_none()
