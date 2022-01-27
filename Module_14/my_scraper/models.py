from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from scrapy.utils.project import get_project_settings

from datetime import datetime


Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get('CONNECTION_STRING'))


def create_table(engine):
    Base.metadata.create_all(engine)


class Authors(Base):
    __tablename__ = 'authors_table'

    id = Column(Integer, primary_key=True)
    authors = Column('authors', String(), unique=True)
    author_link = Column('author_link', String())
    inserted_date = Column(DateTime, default=datetime.now())
    authors_conn = relationship('Quotes', back_populates='quotes_conn')


class Quotes(Base):
    __tablename__ = 'quotes_table'

    id = Column(Integer, primary_key=True)
    tags = Column('tags', String())
    quotes = Column('quotes', Text(), unique=True)
    author_id = Column(Integer, ForeignKey('authors_table.id'))
    inserted_date = Column(DateTime, default=datetime.now())
    quotes_conn = relationship('Authors', back_populates='authors_conn')
