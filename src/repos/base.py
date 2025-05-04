from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepos:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **by_filters):
        query = select(self.model).filter_by(**by_filters)
        result = await self.session.execute(query)
        await self.session.commit()
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        add_smth = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(add_smth)
        await self.session.commit()
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, hotel_id, room_id, data: BaseModel,):
        stmt = (
                update(self.model)
                .where(self.model)
                .values(data.model_dump())
        )
        await self.session.execute(stmt)
        return {'status': f'datas in ___ #{id} are fully updated'}

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
        return {'status': f'{filter_by} has been deleted'}

    async def checking(self, data_id: int):
        stmt = select(self.model).filter(self.model.id == data_id)
        data = await self.session.execute(stmt)
        data = data.scalars().one_or_none()
        if data is None:
            raise HTTPException(status_code=404, detail=f'The data is not found!')
