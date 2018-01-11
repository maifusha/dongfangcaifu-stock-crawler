# -*- coding: utf-8 -*-

""" 财经会议模型 """

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime
from crawl.db import BaseModel, ModelMixin


class FinancialMeeting(BaseModel, ModelMixin):
    __tablename__ = 'financial_meetings'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    title = Column(String(256))
    organizer = Column(String(128))
    region = Column(String(32))
    type = Column(String(32))
    relate_plates = Column(String(64))
    relate_codes = Column(String(32))
