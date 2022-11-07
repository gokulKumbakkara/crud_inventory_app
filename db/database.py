
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///main_database.db",echo=True,connect_args={'check_same_thread': False})
Base = declarative_base()


class inventory(Base):
    __tablename__="inventories"
    id = Column(Integer,primary_key=True)
    items = Column(String(100))
    user_id = Column(Integer,ForeignKey('users.id'))

    inventory_relation= relationship("user_table",back_populates='user_relation')

class user_table(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True)
    name=Column(String(100))
    email=Column(String(100))
    password=Column(String(100))

    user_relation= relationship("inventory",back_populates='inventory_relation')