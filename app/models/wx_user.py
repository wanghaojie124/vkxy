from app.models.base import Base, db
from sqlalchemy import Column, Integer, String


class WxUser(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(20))
    gender = Column(Integer)
    city = Column(String(20))
    province = Column(String(20))
    avatar_url = Column(String(255))
    openid = Column(String(255))
    session_key = Column(String(255))
    uid = Column(Integer)
