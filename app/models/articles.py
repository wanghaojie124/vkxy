from sqlalchemy.orm import relationship
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey


class Articles(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    intro = Column(String(255))
    weight = Column(Integer)
    on_index = Column(Integer, default='0')
    type = Column(String(25))
    link = Column(String(255))
    image = Column(String(255))
    content = Column(String(255))
    college = Column(String(64))

    # college = relationship('Colleges')
    # cid = Column(Integer, ForeignKey('college.id'))
    