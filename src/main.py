from fastapi import FastAPI
import uvicorn
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
