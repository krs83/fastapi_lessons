from datetime import date

from pydantic import BaseModel

from src.models.m_hotels import HotelsOrm
from src.models.m_rooms import RoomsOrm
from src.repos.base import BaseRepos
from sqlalchemy import select, insert, delete, func, update

from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking


class HotelsRepos(BaseRepos):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
            self,
            location,
            title,
            offset,
            limit,
            date_to: date,
            date_from: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        if location:
            hotels_ids_to_get = (hotels_ids_to_get
                                 .filter(func.lower(HotelsOrm
                                                    .location)
                                         .contains(location.strip()
                                                   .lower())))
        if title:
            hotels_ids_to_get = (hotels_ids_to_get.
                                 filter(func.lower(HotelsOrm.title)
                                        .contains(title.strip()
                                                  .lower())))

        hotels_ids_to_get = (
            hotels_ids_to_get
            .limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))

    async def get_hotel(self, hotel_id: int):
        stmt = select(self.model).where(self.model.id == hotel_id)
        hotel = await self.session.execute(stmt)
        hotel = hotel.scalars().one()
        return hotel

    async def add(self, hotel_info):
        add_hotel = insert(self.model).values(**hotel_info.model_dump()).returning(self.model)
        res = await self.session.execute(add_hotel)
        hotel = res.scalars().one()
        return self.mapper.map_to_domain_entity(hotel)

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
