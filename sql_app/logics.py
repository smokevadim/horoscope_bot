import datetime

from sqlalchemy.orm import Session

from . import schemas, models


def create_horoscope(db: Session, horoscope: schemas.HoroscopeCreate):
    horoscope = models.Horoscope(
        date=horoscope.date,
        zodiac=horoscope.zodiac,
        horoscope=horoscope.horoscope
    )
    in_db = db.query(models.Horoscope).filter_by(
        date=horoscope.date,
        zodiac=horoscope.zodiac).first()
    if in_db:
        in_db.horoscope = horoscope.horoscope
        instance = in_db
    else:
        db.add(horoscope)
        instance = horoscope
    db.commit()
    db.refresh(instance)
    return instance


