from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserScore(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    xh = Column(String(64))
    name = Column(String(25))
    course = Column(String(255))
    xuanxiu = Column(String(25))
    score = Column(String(64))
    jidian = Column(String(20))
    xueqi = Column(String(25))
    xuefen = Column(Float)
    xishu = Column(Float)

