from fastapi import APIRouter

from src.schemas.schem_facilities import FacilitiesAdd, FacilitiesPut
from src.api.dependency import DBDep

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/all')
async def get_all_facilities(
        db: DBDep,
        id: int | None = None,
        title: str | None = None
):
    return await db.facilities.get_all(id, title)


@router.post('')
async def create_facilities(
        db: DBDep,
        facilities_data: FacilitiesAdd
):
    await db.facilities.add(facilities_data)
    await db.commit()
    return facilities_data


@router.delete('/{facility_id}')
async def delete_facility(facility_id: int,
                          db: DBDep,
                          ):
    await db.facilities.delete_by_id(facility_id)
    await db.commit()
    return {'status': f'The facility has been deleted'}


@router.put('/{facility_id}}')
async def update_facility(
        id: int,
        db: DBDep,
        facility_data: FacilitiesPut):
    await db.facilities.edit_facility(id, facility_data)
    await db.commit()
    return {'status': f'The facility has been updated'}
