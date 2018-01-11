# -*- coding: utf-8 -*-

""" 流通股东模型 """

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime
from crawl.db import BaseModel, ModelMixin


class CirculationShareholder(BaseModel, ModelMixin):
    __tablename__ = 'circulation_shareholders'

    id = Column(Integer, primary_key=True)
    code = Column(CHAR(6))
    date = Column(Date)
    index = Column(SmallInteger)
    name = Column(String(256))
    nature = Column(String(32))
    share_num = Column(BigInteger)
    share_ratio = Column(Float)
    share_change = Column(BigInteger)
    share_change_ratio = Column(Float)
    share_state = Column(Integer)
    created_at = Column(DateTime)