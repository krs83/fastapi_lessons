from fastapi import APIRouter

from src.schemas.schem_bookings import BookingsAdd
from src.api.dependency import DBDep, UserIdDep, PaginationDep

router = APIRouter(prefix='/bookings', tags=['Бронирование'])


@router.get('/bookings')
async def get_all_bookings(db: DBDep):
    all_booking = await db.bookings.get_all()
    await db.commit()
    return all_booking


@router.get('/me')
async def get_my_booking(db: DBDep,
                         user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    my_bookings = await db.bookings.get_all(user_id=user.id)
    await db.commit()
    return my_bookings


@router.post('')
async def book(data: BookingsAdd,
               db: DBDep,
               user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    price = await db.rooms.get_room_price(data.room_id)
    booking = await db.bookings.add_bookings(data, user.id, price)
    await db.commit()
    return booking
