from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg2://postgres:pstgr_28.09_ig@localhost:5432/module_9.hw')
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


class AddressBook(Base):
    __tablename__ = 'address_book'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)

    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __repr__(self):
        return f"{self.name},{self.phone},{self.email},{self.address}"


Base.metadata.create_all(engine)
Base.metadata.bind = engine
