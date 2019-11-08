from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserSchedule(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    xh = Column(Integer, nullable=True)
    name = Column(String(25))
    jie = Column(String(20))
    Mon = Column(String(255), default="")
    Tues = Column(String(255), default="")
    Wed = Column(String(255), default="")
    Thur = Column(String(255), default="")
    Fri = Column(String(255), default="")
    Sat = Column(String(255), default="")
    Sun = Column(String(255), default="")
