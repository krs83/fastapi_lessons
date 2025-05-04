from pydantic import BaseModel

from src.models.m_hotels import HotelsOrm
from src.repos.base import BaseRepos
from sqlalchemy import select, insert, delete, func, update

from src.schemas.schem_hotels import Hotel


class HotelsRepos(BaseRepos):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      location,
                      title,
                      offset,
                      limit) -> list[Hotel]:

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
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_hotel(self, hotel_id: int):
        stmt = select(self.model).where(self.model.id == hotel_id)
        hotel = await self.session.execute(stmt)
        hotel = hotel.scalars().one()
        return hotel

    async def add(self, hotel_info):
        add_hotel = insert(self.model).values(**hotel_info.model_dump()).returning(self.model)
        res = await self.session.execute(add_hotel)
        hotel = res.scalars().one()
        return Hotel.model_validate(hotel, from_attributes=True)

    async def delete_by_id(self, hotel_id: int) -> None:
        await self.checking(hotel_id)
        stmt = delete(self.model).where(self.model.id == hotel_id)
        await self.session.execute(stmt)

    async def edit(self, hotel_id, data: BaseModel, unset: bool = False) -> None:
        await self.checking(hotel_id)
        stmt = (
            update(self.model)
            .where(self.model.id == hotel_id)
            .values(data.model_dump(exclude_unset=unset))
        )
        await self.session.execute(stmt)

