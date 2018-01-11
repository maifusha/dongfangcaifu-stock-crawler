# -*- coding: utf-8 -*-
import scrapy
from crawl import db
import time
from crawl.models.Information import Information

class InformationSpider(scrapy.Spider):
    name = "information"
    allowed_domains = ["www.cs.com.cn"]
    start_urls = ['http://www.cs.com.cn/ssgs/gsxw/']
    url_tpl = {
        'page':'http://www.cs.com.cn/ssgs/gsxw/index_s%.shtml',
        'base_url':'http://www.cs.com.cn/ssgs/gsxw',
    }

    # 爬虫结束后关闭数据库连接
    def close(spider,reason):
        db.session.close()
    #打印
    def dump(self,content):
        print '################################'
        print content
        print '################################'
    #处理详情页的url
    def handl_url(self,url):
        #由于取出来deurl是./201708/t20170804_5408388.html
        url = url[1:len(url)] #去除第一个点
        allurl = self.url_tpl['base_url'] + url#同基础url拼接完整的连接
        return allurl
    #处理时间
    #def handl_time(self,infor_time):
    #保存到表中
    #def save_information(self,information_data):
        #self.dump(information_data)
        #information = Information(**information_data)

        #information.save()
    #############################################
    # 从start_url里分析出来第一个的连接数量
    def parse(self, response):
        infor = response.css('.box740 dl')
        for dl in infor:
            # 详情页面的url
            detail_url = self.handl_url(dl.xpath('dt/a/@href').extract_first())
            # 资讯标题
            infor_title = dl.xpath('dt/a/text()').extract_first()
            # 去重判断
            #抓详情页面
            yield scrapy.Request(detail_url, callback=self.detail_parse)
        pass
    #详情页面的回调函数
    def detail_parse(self,response):
        #标题
        #title = response.css('.artical_t').xpath('h1/text()').extract_first()
        #时间：
        #create_at = response.css('.artical_t .Ff').xpath('text()').extract_first()
        #内容
        #content = response.css('.artical_c').extract_first()
        #来源：
        #author = response.css('.artical_t').xpath('span[2]/text()').extract_first()
        information = {
            'title':response.css('.artical_t').xpath('h1/text()').extract_first(),
            'img':'1',
            'source':response.css('.artical_t').xpath('span[2]/text()').extract_first(),
            'content': response.css('.artical_c').extract_first(),
            'author':'1',
            'pub_time':response.css('.artical_t .Ff').xpath('text()').extract_first(),
            'status':0,
            'news_type':1,
            'created_at':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        }
        #self.save_information(information)
        self.dump(information)


