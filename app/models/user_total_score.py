from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserTotalScore(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    xh = Column(String(64))
    name = Column(String(25))
    total_xuefen = Column(Float, comment='目前已修总学分')
    average_score = Column(Float, comment='历年平均成绩')
    average_jidian = Column(Float, comment='历年平均绩点')
