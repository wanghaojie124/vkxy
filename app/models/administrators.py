from app import login_manager
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin


class Administrators(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(64), nullable=False)

    @login_manager.user_loader
    def get_user(uid):
        return Administrators.query.get(int(uid))