from sqlalchemy import Column, ForeignKey, Integer, String,Boolean,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from fastapi import Request


engine = create_engine(
    "sqlite:///main_database.db", echo=True, connect_args={"check_same_thread": False}
)
Base = declarative_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



class inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True)
    items = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))

    inventory_relation = relationship("user_table", back_populates="user_relation")


class user_table(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    is_superuser = Column(Boolean())

    user_relation = relationship("inventory", back_populates="inventory_relation")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 