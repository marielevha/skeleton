from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ad(Base):
    __tablename__ = "ad"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String)
    city = Column('city', String)


# engine = create_engine('sqlite:///skeleton.sqlite3', echo=True)
# Base.metadata.create_all(bind=engine)


import schedule
import time


def good_lick():
    print('Good Luck for Test')


def work():
    print('Study and work hard')


schedule.every(10).seconds.do(good_lick)

while True:
    schedule.run_pending()
    # time.sleep(1)
