# -*- coding: utf-8 -*-

""" 股票名单模型 """

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime
from crawl.db import BaseModel, ModelMixin


class Stock(BaseModel, ModelMixin):
    __tablename__ = 'stocks'

    code = Column(CHAR(6), primary_key=True)
    exchange = Column(CHAR(2))
    company_name = Column(String(32))
    industry_sector_num = Column(CHAR(12))
    launch_date = Column(Date)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)