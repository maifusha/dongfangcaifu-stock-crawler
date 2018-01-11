# -*- coding: utf-8 -*-

""" 股票名单模型 """

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime
from crawl.db import BaseModel, ModelMixin


class StockOld(BaseModel, ModelMixin):
    __tablename__ = 'stock_olds'

    code = Column(CHAR(6), primary_key=True)
    exchange = Column(CHAR(2))
    company_name = Column(String(32))
    launch_date = Column(Date)
    csrc_code = Column(CHAR(1))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)