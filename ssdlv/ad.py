from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ad(Base):
    __tablename__ = "ad"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String)
    city = Column('city', String)


engine = create_engine('sqlite:///scraper.sqlite', echo=True)
Base.metadata.create_all(bind=engine)
