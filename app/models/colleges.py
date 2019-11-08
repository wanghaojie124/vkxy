from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean


class Colleges(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    college_name = Column(String(64), unique=True)
    use_code = Column(Integer)
