from pydantic import BaseModel, ConfigDict, Field


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilitiesPut(BaseModel):
    title: str
