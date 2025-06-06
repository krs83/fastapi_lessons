from datetime import date

from src.models.m_booking import BookingOrm
from src.models.m_rooms import RoomsOrm
from sqlalchemy import select, func


def rooms_ids_for_booking(
        date_to: date,
        date_from: date,
        hotel_id: int | None = None
):
    rooms_count = (
        select(BookingOrm.room_id, func.count('*').label('room_booked'))
        .select_from(BookingOrm)
        .filter(
            BookingOrm.date_to <= date_from,
            BookingOrm.date_from >= date_to,
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

    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel
        .subquery(name='rooms_ids_for_hotel')
    )

    rooms_ids_to_get = (
        select(rooms_left_c.c.room_id)
        .select_from(rooms_left_c)
        .filter(rooms_left_c.c.rooms_left > 0,
                rooms_left_c.c.room_id.in_(rooms_ids_for_hotel)
                )
    )
    return rooms_ids_to_get
