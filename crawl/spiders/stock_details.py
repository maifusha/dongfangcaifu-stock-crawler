# -*- coding: utf-8 -*-

""" 东方财富网：个股详情爬虫 """

import re
import scrapy
import json
import time
from crawl import db
from crawl import helper
from crawl.models.Stock import Stock
from crawl.models.StockDetail import StockDetail


class StockDetailsSpider(scrapy.Spider):
    name = "stock_details"
    allowed_domains = ["quote.eastmoney.com", "nuff.eastmoney.com"]

    pattern = r'QaDefault\((.*?)\)' #匹配页面数据信息的正则
    uri_tpl = {
        'page': 'http://quote.eastmoney.com/%s%s.html',
        'inf' : 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=%s%s',
    }
    exchange2market_map = {
        'sh': 1,
        'sz': 2,
    }

    # 初始化爬虫时，预先编译好正则表达式
    def __init__(self, *args, **kwargs):
        super(StockDetailsSpider, self).__init__(*args, **kwargs) #调用父类方法
        self.pattern = re.compile(self.pattern)

    # 自定义框架内置的抓取启动方法
    def start_requests(self):
        for stock in Stock.query().all():
            yield scrapy.Request(self.page_url(stock), callback=self.parse_page, meta={'stock': stock})

    # 爬虫结束后关闭数据库连接
    def closed(spider, reason):
        db.session.close()

    ###########################################################################################################################

    def page_url(self, stock):
        url = self.uri_tpl['page'] % (stock.exchange, stock.code)
        return url

    def inf_url(self, stock):
        market = self.exchange2market_map[stock.exchange]
        url = self.uri_tpl['inf'] % (stock.code, market)
        return url

    def parse_page(self, response):
        stock = response.meta['stock']
        status = int(self.pattern.search(response.body).group(1).split(',')[10].strip(" '"))

        if status == 1: #上市中的股票，进一步接口请求其详细数据
            yield scrapy.Request(self.inf_url(stock), callback=self.parse_inf, meta={'stock': stock})
        else: #各种异常的股票，直接入库
            stock_detail = {
                'code': stock.code,
                'close_price': None,
                'turnover_ratio': None,
                'pe_ratio': None,
                'pb_ratio': None,
                'total_market_capitalisation': None,
                'circulation_market_capitalisation': None,
                'status': status,
            }

            self.save_stock_detail(stock_detail)

    def parse_inf(self, response):
        stock = response.meta['stock']
        data = json.loads(response.body[9:-1], encoding='utf-8')['Value']

        stock_detail = {
            'code': stock.code,
            'close_price': helper.filter_value(data[34], float),
            'turnover_ratio': helper.filter_value(data[37], float),
            'pe_ratio': helper.filter_value(data[38], float),
            'pb_ratio': helper.filter_value(data[43], float),
            'total_market_capitalisation': helper.filter_value(data[46], int),
            'circulation_market_capitalisation': helper.filter_value(data[45], int),
            'status': int(data[44]),
        }

        self.save_stock_detail(stock_detail)

    def save_stock_detail(self, stock_detail):
        today = time.strftime("%Y-%m-%d", time.localtime())
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        stock_detail['date'] = today
        stock_detail['created_at'] = now
        stock_detail['updated_at'] = now

        StockDetail.create(stock_detail)