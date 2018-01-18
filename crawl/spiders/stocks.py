# -*- coding: utf-8 -*-

""" A股名单爬虫：抓东方财富网 """

import re
import scrapy
import json
import time
from crawl import db
from crawl import helper
from crawl.models.Stock import Stock


class StocksSpider(scrapy.Spider):
    name = "stocks"
    allowed_domains = ["hqres.eastmoney.com", "nufm.dfcfw.com", "quote.eastmoney.com"]
    start_urls = ['http://hqres.eastmoney.com/EMQuote_Center2.0/js/list.min.js']

    token = None
    page_index = None
    page_total = None
    uri_tpl = {
        'page': 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=A&sortRule=1&js={"list":[(x)],"page_total":(pc)}&token=%s&page=%d',
        'detail': 'http://quote.eastmoney.com/%s%s.html',
    }
    exchange_map = {
        '1': 'sh',
        '2': 'sz',
    }

    # 爬虫结束后关闭数据库连接
    def closed(spider, reason):
        db.session.close()

    ###########################################################################################################################

    # 从start_url里分析出接口token
    def parse(self, response):
        # 先模糊分析出其中一段关键文本，缩小搜索氛围和噪声
        fuzz_pattern = r'function ADataModel(.*?)function CFGDataModel'
        fuzz_txt = re.search(fuzz_pattern, response.body, re.S).group(1)

        # 捕获出token值
        token_pattern = r'token=(.*?)&'
        self.token = re.search(token_pattern, fuzz_txt).group(1)

        # 开始轮询股票列表
        yield scrapy.Request(self.page_url(1), callback=self.parse_page)


    def page_url(self, page_index):
        url = self.uri_tpl['page'] % (self.token, page_index)
        return url

    def parse_page(self, response):
        resp = json.loads(response.body)

        # 页码初始化
        if self.page_index == None:
            self.page_index = 1
            self.page_total = int(resp['page_total'])

        for item in resp['list']:
            item = item.encode('utf-8').split(',')

            #不完整的股票信息
            stock = {
                'exchange': helper.filter_value(self.exchange_map[item[0]], str),
                'code': helper.filter_value(item[1], str),
                'company_name': helper.filter_value(item[2], str),
            }

            #进入详情页获取其他信息
            yield scrapy.Request(self.detail_url(stock['exchange'], stock['code']), callback=self.parse_detail, meta={'stock':stock})

        if self.page_index < self.page_total:
            self.page_index = self.page_index + 1
            next_page = self.page_url(self.page_index)
            yield scrapy.Request(next_page, callback=self.parse_page)


    def detail_url(self, stock_exchange, stock_code):
        url = self.uri_tpl['detail'] % (stock_exchange, stock_code)
        return url

    def parse_detail(self, response):
        stock = response.meta['stock']
        stock['industry_sector_num'] = helper.filter_value(response.xpath('//div[@class="nav"]/a[3]/@href').re_first(u'#(\d[\d_]*)'), str, encode='utf-8')
        stock['launch_date'] = helper.filter_value(response.xpath('//table[@id="rtp2"]/tbody/tr[last()]/td/text()').re_first(u'上市时间：(.*)'), str, encode='utf-8')

        self.save_stock(stock)


    def save_stock(self, stock_data):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        stock = Stock(**stock_data)
        stock.updated_at = now
        if not Stock.find(stock_data['code']):
            stock.created_at = now

        stock.save()
