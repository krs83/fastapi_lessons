from datetime import date

from fastapi import APIRouter, Query

from src.api.dependency import PaginationDep, DBDep
from src.schemas.schem_hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None),
        location: str | None = Query(None),
        date_to: date = Query(example='2025-07-01'),
        date_from: date = Query(example='2025-11-18')
):
    offset = (pagination.page - 1) * pagination.per_page
    limit = pagination.per_page
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        offset=offset,
        limit=limit,
        date_to=date_to,
        date_from=date_from
        )


@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int,
                    db: DBDep):
    return await db.hotels.get_hotel(hotel_id)


@router.post('')
async def create_hotel(
        hotel_data: HotelAdd,
        db: DBDep
):
    await db.hotels.add(hotel_data)
    await db.commit()
    return hotel_data


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int,
                       db: DBDep):
    await db.hotels.delete_by_id(hotel_id)
    await db.commit()
    return {'status': f' The hotel by id #{hotel_id} has been deleted'}


@router.patch('/{hotel_id}')
async def part_update_hotel(
        hotel_id: int,
        db: DBDep,
        hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_id=hotel_id,
                         data=hotel_data,
                         unset=True)
    await db.commit()
    return {'status': f'datas in Hotel #{hotel_id} are updated'}


@router.put('/{hotel_id}')
async def full_update_hotel(
        hotel_id: int,
        db: DBDep,
        hotel_data: HotelAdd):
    await db.hotels.edit(hotel_id=hotel_id,
                         data=hotel_data,
                         unset=False)
    await db.commit()
    return {'status': f'datas in Hotel #{hotel_id} are updated'}
