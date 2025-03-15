from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {'id': 0, 'title': 'Сочи', 'name': 'отель Сочи'},
    {'id': 1, 'title': 'Москва', 'name': 'отель Москва'},
    {'id': 2, 'title': 'Dubai', 'name': 'hotel Dubai'},
]
str_name = 'Название'
str_full_name = 'Полное название'


@app.get('/all-hotels')
def get_hotels(
        id: int | None = Query(None, description='Айди'),
        title: str | None = Query(None, description='название отеля')
):
    return [hotel for hotel in hotels]


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': title
        }
    )
    return {'status': 'ok'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]


@app.patch('/edit-hotels/{hotel_id}')
def part_update_hotel(
        hotel_id: int,
        title: str | None = Query(None, description=str_name),
        name: str | None = Query(None, description=str_full_name)):

    return update_hotel(hotel_id, title, name)


@app.put('/full-edit-hotels/{hotel_id}')
def full_update_hotel(
        hotel_id: int,
        title: str = Query(description=str_name),
        name: str = Query(description=str_full_name)):
    return update_hotel(hotel_id, title, name)


def update_hotel(
        hotel_id: int,
        title: str,
        name: str):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title:
                hotel['title'] = title
            if name:
                hotel['name'] = name
    return {'status': f'datas in Hotel #{hotel_id} are updated'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
