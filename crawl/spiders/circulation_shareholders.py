# -*- coding: utf-8 -*-

""" 东方财富网：流通股东爬虫（已废弃） """

import scrapy
import json
import time
from crawl import db
from crawl import helper
from crawl.models.Stock import Stock
from crawl.models.CirculationShareholder import CirculationShareholder


class CirculationShareholdersSpider(scrapy.Spider):
    name = "circulation_shareholders"
    allowed_domains = ["emweb.securities.eastmoney.com"]

    date_tab = 1  #抓取流通股东的第几个日期Tab项
    uri_tpl = 'http://emweb.securities.eastmoney.com/f10_v2/ShareholderResearch.aspx?type=web&code=%s%s'

    def start_requests(self):
        for stock in Stock.query().order_by('code asc').all():
            yield scrapy.Request(self.shareholder_url(stock), callback=self.parse, meta={'stock': stock})

    # 爬虫结束后关闭数据库连接
    def closed(spider, reason):
        db.session.close()

    ###########################################################################################################################

    def parse(self, response):
        stock = response.meta['stock']
        tab_expression = '//div[@id="sdltgd"]/following-sibling::div[@class="content"]/div/ul/li[%d]/span/text()' % (self.date_tab,)
        date = helper.filter_value(response.xpath(tab_expression).extract_first(), str, 'utf-8')

        # 如果当前股票这一季(date)财报的流通股东数据 没有 OR 已抓取过，则直接跳过不处理
        if not date or self.alreadyCrawled(stock, date):
            return

        for tr in response.xpath('//div[@id="TTCS_Table_Div"]/table[1]/tr[position()>1 and position()<last()]'):
            circulation_shareholder = {
                'code': stock.code,
                'date': date,
                'index': helper.filter_value(tr.xpath('th[1]/em/text()').extract_first(), int),
                'name': helper.filter_value(tr.xpath('td[1]/text()').extract_first(), str,  'utf-8'),
                'nature': helper.filter_value(tr.xpath('td[2]/text()').extract_first(), str, 'utf-8'),
                'share_num': helper.filter_value(self.tr_get_share_num(tr), int),
                'share_ratio': self.tr_get_share_ratio(tr),
                'share_change': self.tr_get_share_change(tr),
                'share_change_ratio': self.tr_get_share_change_ratio(tr),
                'share_state': self.tr_get_share_state(tr),
            }
            self.save_circulation_shareholder(circulation_shareholder)

    def alreadyCrawled(self, stock, date):
        crawled = CirculationShareholder.query()\
                    .filter(CirculationShareholder.code==stock.code, CirculationShareholder.date==date)\
                    .count() > 0

        return crawled

    def tr_get_share_num(self, tr):
        share_num = tr.xpath('td[4]/text()').extract_first().replace(',', '')

        return share_num

    def tr_get_share_change(self, tr):
        raw_text = tr.xpath('td[6]/text()').extract_first()
        if raw_text in [u'不变', u'新进']:
            share_change = 0
        else:
            share_change = int(raw_text.replace(',', ''))

        return share_change

    def tr_get_share_ratio(self, tr):
        share_ratio = helper.filter_value(tr.xpath('td[5]/text()').extract_first().rstrip('%').replace(',', ''), float)

        return share_ratio

    def tr_get_share_change_ratio(self, tr):
        share_change_ratio = helper.filter_value(tr.xpath('td[7]/text()').extract_first().rstrip('%').replace(',', ''), float)
        
        return share_change_ratio

    def tr_get_share_state(self, tr):
        raw_text = tr.xpath('td[6]/text()').extract_first()
        if raw_text == u'不变':
            share_state = 0
        elif raw_text == u'新进':
            share_state = 2
        elif '-' in raw_text:
            share_state = -1
        else:
            share_state = 1

        return share_state

    def shareholder_url(self, stock):
        url = self.uri_tpl % (stock.exchange, stock.code)

        return url

    def save_circulation_shareholder(self, circulation_shareholder_data):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        circulation_shareholder = CirculationShareholder(**circulation_shareholder_data)
        circulation_shareholder.created_at = now
        circulation_shareholder.save()
