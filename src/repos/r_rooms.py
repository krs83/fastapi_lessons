from datetime import date

from pydantic import BaseModel

from src.database import engine
from src.models.m_booking import BookingOrm

from src.models.m_rooms import RoomsOrm
from src.repos.base import BaseRepos
from src.schemas.schem_rooms import Rooms
from sqlalchemy import delete, select, func, update


class RoomsRepos(BaseRepos):
    model = RoomsOrm
    schema = Rooms

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
        return [Rooms.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_from: date,
                                   date_to: date):
        rooms_count = (
            select(BookingOrm.room_id, func.count('*').label('room_booked'))
            .select_from(BookingOrm)
            .filter(
                BookingOrm.date_from <= date_to,
                BookingOrm.date_to >= date_from,
            )
            .group_by(BookingOrm.room_id)
            .cte(name='rooms_count')
        )

        rooms_left_c = (
            select(
                RoomsOrm.id.label('room_id'),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.room_booked, 0)).label('rooms_left'),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte('rooms_left_c')
        )

        rooms_id_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name='rooms_id_for_hotel')
        )

        rooms_ids_to_get = (
            select(rooms_left_c.c.room_id)
            .select_from(rooms_left_c)
            .filter(rooms_left_c.c.rooms_left > 0,
                    rooms_left_c.c.room_id.in_(rooms_id_for_hotel)
                    )
        )
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))

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
        data = Rooms.model_validate(data, from_attributes=True)
        return data.price
