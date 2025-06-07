from datetime import date

from pydantic import BaseModel

from src.models.m_facilities import FacilitiesOrm
from src.repos.base import BaseRepos
from src.schemas.schem_facilities import Facilities
from sqlalchemy import delete, select, func, update


class FacilitiesRepos(BaseRepos):
    model = FacilitiesOrm
    schema = Facilities

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




