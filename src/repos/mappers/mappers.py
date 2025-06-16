from src.models.m_booking import BookingOrm
from src.models.m_facilities import FacilitiesOrm
from src.models.m_hotels import HotelsOrm
from src.models.m_rooms import RoomsOrm
from src.models.m_users import UsersOrm
from src.repos.mappers.base import DataMapper
from src.schemas.schem_bookings import Bookings
from src.schemas.schem_facilities import Facilities
from src.schemas.schem_hotels import Hotel
from src.schemas.schem_rooms import Rooms, RoomsWithRels
from src.schemas.schem_users import Users


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomWithResDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = Users


class BookingDataMapper(DataMapper):
    db_model = BookingOrm
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities
