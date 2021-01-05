import datetime
from time import sleep

import requests
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from enums import Zodiac
from settings import AZTRO_SERVER
from sql_app.db import SessionLocal
from sql_app.logics import create_horoscope
from sql_app.schemas import HoroscopeCreate, ListHoroscope, AztroBase

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/update_db", response_model=ListHoroscope)
def update_db(token: str = None, db: Session = Depends(get_db)):
    response_horoscopes = []
    for zodiac in Zodiac:
        horoscope = get_horoscope(zodiac)
        horoscope_in_db = HoroscopeCreate(
            date=horoscope['date'],
            zodiac=horoscope['zodiac'],
            horoscope=horoscope['horoscope']
        )
        response_horoscopes.append(create_horoscope(db=db, horoscope=horoscope_in_db))
    return ListHoroscope(horoscopes=response_horoscopes)


def get_horoscope(zodiac: Zodiac) -> dict:
    return_dict = {}
    params = (
        ('sign', zodiac.name),
        ('day', 'today'),
    )

    response = requests.post(AZTRO_SERVER, params=params)
    sleep(0.5)
    assert response.status_code == 200
    aztro = AztroBase.parse_raw(response.content)
    return_dict['date'] = datetime.datetime.strptime(aztro.current_date, '%B %d, %Y').date()
    return_dict['zodiac'] = zodiac.value
    return_dict['horoscope'] = aztro.description

    return return_dict


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
