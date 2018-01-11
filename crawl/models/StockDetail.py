# -*- coding: utf-8 -*-

""" 个股详情模型 """

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime
from crawl.db import BaseModel, ModelMixin


class StockDetail(BaseModel, ModelMixin):
    __tablename__ = 'stock_details'

    id = Column(Integer, primary_key=True)
    code = Column(CHAR(6))
    date = Column(Date)
    close_price = Column(Float)
    turnover_ratio = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    total_market_capitalisation = Column(BigInteger)
    circulation_market_capitalisation = Column(BigInteger)
    status = Column(SmallInteger)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)