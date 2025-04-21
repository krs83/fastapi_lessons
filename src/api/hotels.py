
from fastapi import APIRouter, Query

from src.api.dependency import PaginationDep
from src.models.m_hotels import HotelsOrm
from src.repos.r_hotels import HotelsRepos
from src.schemas.schem_hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select, func
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
        add_hotel_stmnt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmnt)
        await session.commit()
    return {'status': f'The hotel {hotel_data.title} has been added'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': f'The hotel #{hotel_id} has been deleted'}


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
def full_update_hotel(
        hotel_id: int,
        hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return {'status': f'datas in Hotel #{hotel_id} are fully updated'}

