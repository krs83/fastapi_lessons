from pydantic import BaseModel, ConfigDict, Field

from src.schemas.schem_facilities import Facilities


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsWithRels(Rooms):
    facilities: list[Facilities]


class RoomsPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomsPut(BaseModel):
    title: str
    description: str
    price: int
    quantity: int


class RoomsFacilityPut(RoomsPut):
    facilities_ids: list[int]
