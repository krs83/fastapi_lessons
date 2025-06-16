from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilitiesPut(BaseModel):
    title: str


class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilities(RoomsFacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsFacilitiesPut(BaseModel):
    facility_id: int

    model_config = ConfigDict(from_attributes=True)



