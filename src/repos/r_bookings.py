from sqlalchemy import insert, select, desc

from src.models.m_booking import BookingOrm
from src.repos.base import BaseRepos
from src.schemas.schem_bookings import Bookings


class BookingsRepos(BaseRepos):
    model = BookingOrm
    schema = Bookings

    async def add_bookings(self,
                           data: schema,
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
