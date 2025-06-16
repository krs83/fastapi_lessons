from pydantic import BaseModel

from src.models.m_facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepos
from src.repos.mappers.mappers import FacilityDataMapper
from src.schemas.schem_facilities import RoomsFacilities
from sqlalchemy import delete, update, insert


class FacilitiesRepos(BaseRepos):
    model = FacilitiesOrm
    mapper = FacilityDataMapper

    async def edit_facility(self, facility_id, data: BaseModel) -> None:
        await self.checking(facility_id)
        stmt = (
            update(self.model)
            .where(self.model.id == facility_id)
            .values(data.model_dump())
        )
        await self.session.execute(stmt)

    async def delete_by_id(self, facility_id: int) -> None:
        await self.checking(facility_id)
        stmt = delete(self.model).where(self.model.id == facility_id)
        await self.session.execute(stmt)


class RoomsFacilitiesRepos(BaseRepos):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities

    async def edit_bulk(self, rooms_id, data: list[BaseModel]) -> None:
        new_facility_ids = {f.facility_id for f in data}
        current_facility_ids = await self.get_filtered(room_id=rooms_id)
        current_facility_ids = {f.facility_id for f in current_facility_ids}

        to_remove = current_facility_ids - new_facility_ids
        to_add = new_facility_ids - current_facility_ids

        if to_remove:
            stmt = (
                delete(self.model)
                .where(self.model.room_id == rooms_id)
                .where(self.model.facility_id.in_(to_remove))
            )
            await self.session.execute(stmt)

        if to_add:
            stmt = (
                insert(self.model)
                .values([{"room_id": rooms_id, "facility_id": fid} for fid in to_add])
            )
            await self.session.execute(stmt)
