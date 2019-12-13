from app import login_manager
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    college = Column(String(64))
    name = Column(String(20))
    openid = Column(String(255))
    phone_number = Column(String(18), unique=True)

    def table_is_exist(self, user_id):
        try:
            self.query.filter_by(id=user_id).first()

        except Exception as e:
            print(e)
            return False
        else:
            return True

    # 接收数据
    def save_to_db(self, form):
        if self.query.filter_by(username=form['username']).first():
            with db.auto_commit():
                user = self.query.filter_by(username=form['username']).first()
                user.setattr(form)
            # db.session.commit()
        else:
            with db.auto_commit():
                self.setattr(form)
                db.session.add(self)
                # db.session.commit()

    def save_name(self, username, name, college):
        with db.auto_commit():
            res = self.query.filter_by(username=username).first()
            res.name = name
            res.college = college


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
