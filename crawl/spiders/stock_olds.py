# -*- coding: utf-8 -*-

""" 上证所/深圳所：A股名单爬虫（已废弃） """

import scrapy
import json
import time
from crawl import db
from crawl.models.Stock import Stock


class StockOldsSpider(scrapy.Spider):
    name = "stock_olds"
    allowed_domains = ["www.szse.cn", "query.sse.com.cn"]

    # 抓取地址uri模板
    uri_tpl = {
        'sz': 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=%d&CATALOGID=%d&TABKEY=%s&tab2PAGENO=%d',
        'sh': 'http://query.sse.com.cn/security/stock/getStockListData2.do?pageHelp.cacheSize=%d&stockType=%d&pageHelp.beginPage=%d',
    }

    # 重写框架默认的start_urls处理方法
    # 这里yield弹出并行爬取的支线起点，但每条支线中的爬取是串行的
    def start_requests(self):
        yield scrapy.Request(self.sz_page_url(1), callback=self.sz_parse, headers=self.sz_headers)
        #yield scrapy.Request(self.sh_page_url(1), callback=self.sh_parse, headers=self.sh_headers) #TODO：第一次抓取结束后启用这里

    # 爬虫结束后关闭数据库连接
    def closed(spider, reason):
        db.session.close()


    ################################################## 深圳股票名单处理 #######################################################
    sz_page_index = None
    sz_page_total = None
    sz_headers = {
    }
    sz_params = {
        'ACTIONID': 7,
        'CATALOGID': 1110,
        'TABKEY': 'tab2',
    }

    def sz_page_url(self, page_index):
        url = self.uri_tpl['sz'] % (self.sz_params['ACTIONID'], self.sz_params['CATALOGID'], self.sz_params['TABKEY'], page_index)
        return url

    def sz_parse(self, response):
        # 页码初始化
        if self.sz_page_index == None:
            self.sz_page_index = 1
            self.sz_page_total = int(response.xpath('//table[@id="REPORTID_tab2"]/following-sibling::table//td[@align="left"]/text()').re_first(u'共(.*)页'))

        for stock in self.sz_get_stocks_from_page(response):
            self.save_stock(stock)

        if self.sz_page_index < self.sz_page_total:
            self.sz_page_index = self.sz_page_index + 1
            next_page = self.sz_page_url(self.sz_page_index)
            yield scrapy.Request(next_page, callback=self.sz_parse)
        else:
            #TODO：第一次抓取结束后删除这里
            yield scrapy.Request(self.sh_page_url(1), callback=self.sh_parse, headers=self.sh_headers)

    def sz_get_stocks_from_page(self, response):
        for tr in response.xpath('//table[@id="REPORTID_tab2"]/tr[position()>1]'):
            stock = {
                'code': tr.xpath('td[1]//text()').extract_first().encode('utf-8'),
                'exchange': 'sz',
                'company_name': tr.xpath('td[2]//text()').extract_first().encode('utf-8'),
                'launch_date': tr.xpath('td[5]//text()').extract_first().encode('utf-8'),
                'csrc_code': tr.xpath('td[8]//text()').extract_first()[0].encode('utf-8'),
            }

            yield stock
    ###########################################################################################################################


    ################################################## 上海股票名单处理 #######################################################
    sh_page_index = None
    sh_page_total = None
    sh_headers = {
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
    }
    sh_params = {
        'cacheSize': 1,
        'stockType': 1,
    }

    def sh_page_url(self, page_index):
        url = self.uri_tpl['sh'] % (self.sh_params['cacheSize'], self.sh_params['stockType'], page_index)
        return url

    def sh_parse(self, response):
        resp = json.loads(response.body)

        # 页码初始化
        if self.sh_page_index == None:
            self.sh_page_index = 1
            self.sh_page_total = int(resp['pageHelp']['pageCount'])

        for stock in self.sh_get_stocks_from_page(resp):
            self.save_stock(stock)

        if self.sh_page_index < self.sh_page_total:
            self.sh_page_index = self.sh_page_index + 1
            next_page = self.sh_page_url(self.sh_page_index)
            yield scrapy.Request(next_page, callback=self.sh_parse)
        else:
            pass

    def sh_get_stocks_from_page(self, response):
        for item in response['result']:
            launch_date = item['LISTING_DATE'].encode('utf-8')

            stock = {
                'code': item['COMPANY_CODE'].encode('utf-8'),
                'exchange': 'sh',
                'company_name': item['COMPANY_ABBR'].encode('utf-8'),
                'launch_date': (launch_date!='-' and launch_date or None),
                'csrc_code': '', #TODO：进入详情页去抓取行业门类编码
            }

            yield stock
    ###########################################################################################################################


    ####################################################### 数据持久化处理 ####################################################
    def save_stock(self, stock_data):
        stock = Stock.find(stock_data['code'])
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        if not stock:
            stock_data['created_at'] = now
            stock_data['updated_at'] = now
            Stock.create(stock_data)
        elif stock.company_name!=stock_data['company_name'] or stock.csrc_code!=stock_data['csrc_code']:
            stock.updated_at = now
            stock.company_name = stock_data['company_name']
            stock.csrc_code = stock_data['csrc_code']
            stock.save()
