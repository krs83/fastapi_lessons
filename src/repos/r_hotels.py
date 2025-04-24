from fastapi import HTTPException
from pydantic import BaseModel

from src.models.m_hotels import HotelsOrm
from src.repos.base import BaseRepos
from sqlalchemy import select, insert, delete, func, update


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

    async def add(self, hotel_info):
        add_hotel = insert(self.model).values(**hotel_info.model_dump())
        await self.session.execute(add_hotel)
        await self.session.commit()
        return {'status': f'The hotel {hotel_info.title} has been added'}

    async def delete_by_id(self, hotel_id):
        await self.checking(hotel_id)
        stmt = delete(self.model).where(self.model.id == hotel_id)
        await self.session.execute(stmt)
        await self.session.commit()

        return {'status': f' The hotel by id #{hotel_id} has been deleted'}

    async def edit(self, hotel_id, data: BaseModel, unset: bool = False):
        await self.checking(hotel_id)
        stmt = (
            update(self.model)
            .where(self.model.id == hotel_id)
            .values(data.model_dump(exclude_unset=unset))
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return {'status': f'datas in Hotel #{hotel_id} are updated'}

    async def checking(self, hotel_id):
        stmt = select(self.model).where(self.model.id == hotel_id)
        hotel = await self.session.execute(stmt)
        hotel = hotel.scalars().one_or_none()
        if hotel is None:
            raise HTTPException(status_code=404, detail=f'The Hotel #{hotel_id} is not found!')