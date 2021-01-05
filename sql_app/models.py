from sqlalchemy import Column, Integer, Date, SmallInteger, Text

from sql_app.db import Base


class Horoscope(Base):
    __tablename__ = 'main_horoscope'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, doc='Date')
    zodiac = Column(SmallInteger, doc='Zodiac')
    horoscope = Column(Text, doc='Horoscope')