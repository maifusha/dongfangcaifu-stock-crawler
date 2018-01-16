# -*- coding: utf-8 -*-

""" ORM公共层 """

import os
import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


""" 数据库连接 """
_con_params = (
    'mysql',
    'mysqldb',
    os.environ.get('MYSQL_USERNAME'),
    os.environ.get('MYSQL_PASSWORD'),
    os.environ.get('MYSQL_HOST'),
    os.environ.get('MYSQL_PORT'),
    os.environ.get('MYSQL_DATABASE'),
)
_engine = create_engine('%s+%s://%s:%s@%s:%s/%s' % _con_params)
_session_factory = sessionmaker(bind=_engine)
session = _session_factory()


""" 模型基类 """
class ModelMixin:
    @classmethod
    def query(cls):
        return session.query(cls)

    @classmethod
    def create(cls, data):
        if type(data) ==  types.DictType:
            record = cls(**data)
        else:
            record = data
        session.add(record)
        session.commit()
        return reload

    @classmethod
    def find(cls, id):
        return cls.query().get(id)

    def save(self):
        session.merge(self)
        session.commit()

BaseModel = declarative_base()