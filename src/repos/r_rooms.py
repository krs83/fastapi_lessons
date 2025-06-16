from datetime import date

from pydantic import BaseModel

from src.models.m_rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import RoomDataMapper, RoomWithResDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.schem_rooms import Rooms
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select, func, update


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_all(self,
                      title,
                      description,
                      price,
                      quantity) -> list[Rooms]:

        query = select(RoomsOrm)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if price:
            query = query.filter(RoomsOrm.price == price)
        if quantity:
            query = query.filter(RoomsOrm.quantity == quantity)

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(room) for room in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_to: date,
                                   date_from: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)

        return [RoomWithResDataMapper.map_to_domain_entity(model) for model in result.scalars().all()]

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
        return RoomWithResDataMapper.map_to_domain_entity(model)

    async def delete_room(self, hotel_id, room_id) -> None:
        stmt = (delete(self.model)
                .where(self.model
                       .hotel_id == hotel_id)
                .where(self.model.id == room_id))
        await self.session.execute(stmt)

    async def get_hotel_rooms(self, hotel_id: int):
        stmt = select(self.model).where(self.model.hotel_id == hotel_id)
        rooms = await self.session.execute(stmt)
        rooms = rooms.scalars().all()
        return rooms

    async def edit(self, hotel_id, rooms_id, data: BaseModel, unset: bool = False) -> None:
        stmt = (
            update(self.model)
            .where(self.model.hotel_id == hotel_id)
            .where(self.model.id == rooms_id)
            .values(data.model_dump(exclude_unset=unset))
        )
        await self.session.execute(stmt)

    async def get_room_price(self, room_id):
        stmt = select(self.model).filter(self.model.id == room_id)

        data = await self.session.execute(stmt)
        data = data.scalars().one()
        data = self.mapper.map_to_domain_entity(data)
        return data.price
