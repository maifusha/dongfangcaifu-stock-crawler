# -*- coding: utf-8 -*-

""" 资讯模型"""
from sqlalchemy import Column, SmallInteger, Integer, BigInteger, Float, CHAR, String, Date, DateTime, Text
from crawl.db import BaseModel, ModelMixin
#import pdb
class Information (BaseModel, ModelMixin):
    __table__ = 'information'
    #pdb.set_trace()
    id = Column(Integer, primary_key=True)
    title = Column(String)
    source = Column(String)
    content = Column(Text)
    pub_time = Column(DateTime)
    status = Column(SmallInteger)
    news_type =Column(SmallInteger)
