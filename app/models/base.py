import json
from contextlib import contextmanager
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, Integer, Float, String
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class Query(BaseQuery):

    def filter_by(self, **kwargs):
        # 定义软删除后开启
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=Query)
# db = SQLAlchemy()


def to_json(inst, cls):
    d = dict()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        d[c.name] = v
    # return json.dumps(d, ensure_ascii=False)
    return json.dumps(d)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {"keep_existing": True}
    status = Column(Integer, default=1)

    def setattr(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # 将model中的字段及属性以json格式返回
    @property
    def serialize(self):
        return to_json(self, self.__class__)
