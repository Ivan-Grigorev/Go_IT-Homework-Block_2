from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, Text, DateTime
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
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(), unique=True)
    author_link = Column('author_link', String())
    inserted_date = Column(DateTime, default=datetime.now())
    quote = relationship('Quotes', back_populates='authors')


class Quotes(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    tags = Column('tags', String())
    quote_content = Column('quotes', Text())
    author_id = Column(Integer, ForeignKey('authors.id'))
    inserted_date = Column(DateTime, default=datetime.now())
    authors = relationship('Authors', back_populates='quote')
