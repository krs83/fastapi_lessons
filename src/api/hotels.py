
from fastapi import APIRouter, Query

from src.api.dependency import PaginationDep
from src.repos.r_hotels import HotelsRepos
from src.schemas.schem_hotels import Hotel, HotelPATCH
from src.database import async_session_maker


router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None),
        location: str | None = Query(None)
):
    async with (async_session_maker() as session):
        offset = (pagination.page - 1) * pagination.per_page
        limit = pagination.per_page
        return await HotelsRepos(session).get_all(location=location,
                                                  title=title,
                                                  offset=offset,
                                                  limit=limit)


@router.post('')
async def create_hotel(
        hotel_data: Hotel
):
    async with async_session_maker() as session:
        return await HotelsRepos(session).add(hotel_data)


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepos(session).delete_by_id(hotel_id)


@router.patch('/{hotel_id}')
def part_update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
        return {'status': f'datas in Hotel #{hotel_id} are partially updated'}


@router.put('/{hotel_id}')
async def full_update_hotel(
        hotel_id: int,
        hotel_data: Hotel):
    async with async_session_maker() as session:
        return await HotelsRepos(session).edit(hotel_id=hotel_id,
                                               data=hotel_data)

