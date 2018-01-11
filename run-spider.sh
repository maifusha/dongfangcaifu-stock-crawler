#!/bin/sh

# 执行指定爬虫，并记录时间到crond日志中
# Example-Use：/srv/crawl/run-spider.sh 爬虫名

now=`date +"%Y-%m-%d %H:%M:%S"`
sed -i "$ s/^/${now} /" /var/log/crond.log
cd /srv/crawl
scrapy crawl $1 --logfile=/var/log/scrapy.log --loglevel=ERROR