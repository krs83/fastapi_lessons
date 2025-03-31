from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(default=3, ge=1, lt=5)]


PaginationDep = Annotated[PaginationParams, Depends()]
