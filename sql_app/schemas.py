import datetime
import json
from typing import List

from pydantic import BaseModel


class HoroscopeBase(BaseModel):
    date: datetime.date
    zodiac: int
    horoscope: str


class HoroscopeCreate(HoroscopeBase):
    pass


class Horoscope(HoroscopeBase):
    id: int

    class Config:
        orm_mode = True


class ListHoroscope(BaseModel):
    horoscopes: List[Horoscope]


class AztroBase(BaseModel):
    date_range: str
    current_date: str
    description: str
    compatibility: str
    mood: str
    color: str
    lucky_number: int
    lucky_time: str
