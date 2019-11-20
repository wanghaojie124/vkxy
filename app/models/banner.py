from app.models.base import Base
from sqlalchemy import Column, Integer, String, DECIMAL


class Banner(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    weight = Column(Integer)
    link = Column(String(255))
    mini = Column(String(255))
    image = Column(String(255))
    college = Column(String(64))
    special = Column(Integer, default=0)
    price = Column(DECIMAL)
    bargain_price = Column(DECIMAL)
