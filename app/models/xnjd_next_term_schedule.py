from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from app.models.base import Base


class XnjdNextTermSchedule(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    xh = Column(String(64))
    name = Column(String(25))
    course_name = Column(String(64))
    course_teacher = Column(String(64))
    course_weeks = Column(String(64))
    class_day = Column(String(64))
    course_address = Column(String(255))
    course_continue = Column(String(64))
