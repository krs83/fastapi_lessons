from fastapi import APIRouter

from src.schemas.schem_bookings import BookingsAdd
from src.api.dependency import DBDep, UserIdDep

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.post('')
async def book(data: BookingsAdd,
               db: DBDep,
               user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    price = await db.rooms.get_room_price(data.room_id)
    booking = await db.bookings.add_bookings(data, user.id, price)
    await db.commit()
    return booking
