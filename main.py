import asyncio
import datetime

import aiohttp
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from enums import Zodiac
from settings import AZTRO_SERVER
from sql_app.db import SessionLocal
from sql_app.logics import create_horoscope
from sql_app.schemas import HoroscopeCreate, ListHoroscope, AztroBase

app = FastAPI()
horoscopes = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/update_db", response_model=ListHoroscope)
def update_db(token: str = None, db: Session = Depends(get_db)) -> ListHoroscope:
    response_horoscopes = []
    horoscopes.clear()
    asyncio.run(get_horoscopes())
    for horoscope in horoscopes:
        horoscope_in_db = HoroscopeCreate(
            date=horoscope['date'],
            zodiac=horoscope['zodiac'],
            horoscope=horoscope['horoscope']
        )
        response_horoscopes.append(create_horoscope(db=db, horoscope=horoscope_in_db))
    return ListHoroscope(horoscopes=response_horoscopes)


async def fetch_remote_server(url, params, session):
    async with session.post(url, params=params) as response:
        assert response.status == 200
        aztro = AztroBase.parse_raw(await response.read())
        horoscope_dict = {
            'date': datetime.datetime.strptime(aztro.current_date, '%B %d, %Y').date(),
            'zodiac': eval(f'Zodiac.{params[0][1]}.value'),
            'horoscope': aztro.description
        }
        horoscopes.append(horoscope_dict)


async def get_horoscopes():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for zodiac in Zodiac:
            params = (
                ('sign', zodiac.name),
                ('day', 'today'),
            )
            task = asyncio.create_task(fetch_remote_server(AZTRO_SERVER, params, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
