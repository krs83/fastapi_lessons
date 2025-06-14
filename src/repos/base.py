from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload

from src.schemas.schem_rooms import RoomsWithRels


class BaseRepos:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **by_filters):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**by_filters)

        )
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomsWithRels.model_validate(model)

    async def add(self, data: BaseModel):
        add_smth = insert(self.model).values(**data.model_dump()).returning(self.model)
        print('*****************')
        print(add_smth)
        res = await self.session.execute(add_smth)
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_smth = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_smth)

    async def edit(self, hotel_id, room_id, data: BaseModel):
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
