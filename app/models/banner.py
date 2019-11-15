from app.models.base import Base
from sqlalchemy import Column, Integer, String, Float


class Banner(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    intro = Column(String(255))
    weight = Column(Integer)
    type = Column(String(25))
    link = Column(String(255))
    mini = Column(String(255))
    image = Column(String(255))
    content = Column(String(255))
    college = Column(String(64))
    special = Column(Integer, default=0)
    price = Column(Float)
    bargain_price = Column(Float)
