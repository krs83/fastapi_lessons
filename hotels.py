from fastapi import Body, APIRouter
from shemas.schem_hotels import Hotel, HotelPATCH

hotels = [
    {'id': 1, 'title': 'Сочи', 'name': 'отель Сочи'},
    {'id': 2, 'title': 'Москва', 'name': 'отель Москва'},
    {'id': 3, 'title': 'Мальдивы', 'name': 'hotel Dubai'},
    {'id': 4, 'title': 'Геледжик', 'name': 'отель Геледжик'},
    {'id': 5, 'title': 'Казань', 'name': 'отель Казань'},
    {'id': 6, 'title': 'Ростов', 'name': 'отель Ростов-на-Дону'},
    {'id': 7, 'title': 'Санкт-Петербург', 'name': 'отель Санкт-Петербург'},
    {'id': 8, 'title': 'Алушта', 'name': 'отель Алушта'},

]

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('')
def get_hotels(
        page: int = 1,
        per_page: int = 3,
):
    start = (page - 1) * per_page
    end = start + per_page

    return [hotel for hotel in hotels[start:end]]


@router.post('')
def create_hotel(
        hotel_data: Hotel
):
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': hotel_data.title,
            'name': hotel_data.name
        }
    )
    return {'status': f'The hotel {hotel_data.title} has been added'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': f'The hotel #{hotel_id} has been deleted'}


@router.patch('/{hotel_id}')
def part_update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
        return {'status': f'datas in Hotel #{hotel_id} are partially updated'}


@router.put('/{hotel_id}')
def full_update_hotel(
        hotel_id: int,
        hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return {'status': f'datas in Hotel #{hotel_id} are fully updated'}

