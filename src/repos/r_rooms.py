from pydantic import BaseModel

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

