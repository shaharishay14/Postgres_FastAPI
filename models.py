from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, Float
from database import Base

class Item(Base):
    __tablename__ = 'Items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    price = Column(Float, index=True)

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    is_verified = Column(Boolean, default=False)

