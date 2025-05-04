from fastapi import APIRouter

from src.database import async_session_maker
from src.repos.r_rooms import RoomsRepos
from src.schemas.schem_rooms import RoomsPatch, RoomsAdd, RoomsPut

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/all/rooms')
async def get_all_rooms(
        title: str | None = None,
        description: str | None = None,
        price: int | None = None,
        quantity: int | None = None
):
    async with (async_session_maker() as session):
        return await RoomsRepos(session).get_all(title=title,
                                                 description=description,
                                                 price=price,
                                                 quantity=quantity)


@router.get('/{hotel_id}/rooms')
async def get_rooms_from_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepos(session).get_hotel_rooms(hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_rooms(
        room_data: RoomsAdd
):
    async with async_session_maker() as session:
        return await RoomsRepos(session).add(room_data)


@router.delete('/{hotel_id}/rooms/{rooms_id}')
async def delete_rooms(hotel_id: int,
                       rooms_id: int):
    async with async_session_maker() as session:
        return await RoomsRepos(session).delete_room(hotel_id, rooms_id)


@router.put('/{hotel_id}/rooms/{rooms_id}')
async def full_update_hotel_room(
        hotel_id: int,
        rooms_id: int,
        room_data: RoomsPut):
    async with async_session_maker() as session:
        return await RoomsRepos(session).edit(hotel_id=hotel_id,
                                              rooms_id=rooms_id,
                                              data=room_data,
                                              unset=False)


@router.patch('/{hotel_id}/rooms/{rooms_id}')
async def part_update_hotel_room(
        hotel_id: int,
        rooms_id: int,
        room_data: RoomsPatch):
    async with async_session_maker() as session:
        return await RoomsRepos(session).edit(hotel_id=hotel_id,
                                              rooms_id=rooms_id,
                                              data=room_data,
                                              unset=True)
