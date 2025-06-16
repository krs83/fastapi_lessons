from sqlalchemy import insert, select, desc

from src.models.m_booking import BookingOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import BookingDataMapper


class BookingsRepos(BaseRepos):
    model = BookingOrm
    mapper = BookingDataMapper

    async def get_all(self, **by_filters):
        query = select(self.model).filter_by(**by_filters)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def add_bookings(self,
                           data: mapper.schema,
                           user: int,
                           price: int):
        add_booking = (
            insert(self.model)
            .values(**data.model_dump())
            .values(user_id=user)
            .values(price=price)
            .returning(self.model))
        res = await self.session.execute(add_booking)
        res.scalars().one()
        total_price = (select(self.model.total_price).
                       filter(self.model.user_id == user).
                       order_by(desc(self.model.id)).limit(1))
        tot_price = await self.session.execute(total_price)
        tot_price = tot_price.scalar()

        days = (data.date_to - data.date_from).days
        return {f"""The user #{user} has booked room #{data.room_id} for {days} days.\n 
        The cost for 1 day is {price}$. Total price is {tot_price}$
        """}
