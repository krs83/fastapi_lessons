from datetime import date

from fastapi import APIRouter, Query

from src.schemas.schem_rooms import RoomsPatch, RoomsAdd, RoomsPut
from src.api.dependency import DBDep

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/all/rooms')
async def get_all_rooms(
        db: DBDep,
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        quantity: int | None = None
):
    return await db.rooms.get_all(title=title,
                                  description=description,
                                  price=price,
                                  quantity=quantity)


@router.get('/{hotel_id}/rooms')
async def get_rooms_from_hotel(hotel_id: int,
                               db: DBDep,
                               date_to: date = Query(example='2025-07-01'),
                               date_from: date = Query(example='2025-11-18')):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_to=date_to, date_from=date_from)


@router.post('/{hotel_id}/rooms')
async def create_rooms(
        db: DBDep,
        room_data: RoomsAdd
):
    await db.rooms.add(room_data)
    await db.commit()
    return room_data


@router.delete('/{hotel_id}/rooms/{rooms_id}')
async def delete_rooms(hotel_id: int,
                       db: DBDep,
                       rooms_id: int):
    await db.rooms.delete_room(hotel_id, rooms_id)
    await db.commit()
    return {'status': f'The room with id #{rooms_id} in hotel #{hotel_id} has been deleted'}


@router.put('/{hotel_id}/rooms/{rooms_id}')
async def full_update_hotel_room(
        hotel_id: int,
        db: DBDep,
        rooms_id: int,
        room_data: RoomsPut):
    await db.rooms.edit(hotel_id=hotel_id,
                        rooms_id=rooms_id,
                        data=room_data,
                        unset=False)
    await db.commit()
    return {'status': f'room data in Hotel #{hotel_id} are updated'}


@router.patch('/{hotel_id}/rooms/{rooms_id}')
async def part_update_hotel_room(
        hotel_id: int,
        db: DBDep,
        rooms_id: int,
        room_data: RoomsPatch):
    await db.rooms.edit(hotel_id=hotel_id,
                        rooms_id=rooms_id,
                        data=room_data,
                        unset=True)
    await db.commit()
    return {'status': f'room data in Hotel #{hotel_id} are updated'}
