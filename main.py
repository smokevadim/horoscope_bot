import datetime

import requests
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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
    for i in range(1, 13):
        horoscope = HoroscopeCreate(
            date=datetime.date.today(),
            zodiac=i,
            horoscope='Good news everyone!'
        )
        response_horoscopes.append(create_horoscope(db=db, horoscope=horoscope))
    return ListHoroscope(horoscopes=response_horoscopes)


def get_horoscope() -> dict:
    params = (
        ('sign', 'aries'),
        ('day', 'today'),
    )

    response = requests.post('https://aztro.sameerkumar.website/', params=params)
    assert response.status_code == 200
    aztro = AztroBase.parse_raw(response.content)

    return {'zodiac': 'aries', 'horoscope': aztro.description}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
