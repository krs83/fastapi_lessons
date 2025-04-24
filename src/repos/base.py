from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


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

    async def add(self, data: BaseModel):
        add_smth = insert(self.model).values(**data.model_dump())
        await self.session.execute(add_smth)
        return {'status': f'{data} has been added'}

    async def edit(self, id, data: BaseModel,):
        stmt = (
                update(self.model)
                .where(self.model)
                .values(data.model_dump())
        )
        await self.session.execute(stmt)
        return {'status': f'datas in ___ #{id} are fully updated'}

    async def delete(self, id):
        stmt = delete(self.model).where(id)
        await self.session.execute(stmt)
        return {'status': f'{id} has been deleted'}
