from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserSchedule(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    xh = Column(String(64))
    name = Column(String(25))
    jie = Column(String(20))
    Mon = Column(TEXT, default="")
    Tues = Column(TEXT, default="")
    Wed = Column(TEXT, default="")
    Thur = Column(TEXT, default="")
    Fri = Column(TEXT, default="")
    Sat = Column(TEXT, default="")
    Sun = Column(TEXT, default="")
    # week = Column(String(255), default="")
