from fastapi import FastAPI
import uvicorn
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.booking import router as router_booking
from src.api.facilities import router as router_facilities

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_booking)
app.include_router(router_facilities)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
