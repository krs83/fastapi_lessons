from src.repos.r_hotels import HotelsRepos
from src.repos.r_rooms import RoomsRepos
from src.repos.r_users import UsersRepos
from src.repos.r_bookings import BookingsRepos


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepos(self.session)
        self.rooms = RoomsRepos(self.session)
        self.users = UsersRepos(self.session)
        self.bookings = BookingsRepos(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()




