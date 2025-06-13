from datetime import date

from fastapi import APIRouter, Query, Body

from src.schemas.schem_rooms import RoomsPatch, RoomsAdd, RoomsPut, RoomsAddRequest, RoomsFacilityPut
from src.schemas.schem_facilities import RoomsFacilitiesAdd, RoomsFacilitiesPut
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
        hotel_id: int,
        db: DBDep,
        room_data: RoomsAddRequest = Body()
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    print(room_data)
    room = await db.rooms.add(_room_data)
    print('from create func')
    print(_room_data)

    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return room_data


@router.put('/{hotel_id}/rooms/{rooms_id}')
async def full_update_hotel_room(
        hotel_id: int,
        db: DBDep,
        rooms_id: int,
        room_data: RoomsFacilityPut):

    _room_data = RoomsPut(**room_data.model_dump())
    await db.rooms.edit(hotel_id=hotel_id,
                        rooms_id=rooms_id,
                        data=_room_data,
                        unset=False
                       )

    rooms_facilities_data = [RoomsFacilitiesPut(facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.edit_bulk(rooms_id=rooms_id, data=rooms_facilities_data, unset=False)
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


@router.delete('/{hotel_id}/rooms/{rooms_id}')
async def delete_rooms(hotel_id: int,
                       db: DBDep,
                       rooms_id: int):
    await db.rooms.delete_room(hotel_id, rooms_id)
    await db.commit()
    return {'status': f'The room with id #{rooms_id} in hotel #{hotel_id} has been deleted'}