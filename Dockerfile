FROM 121.40.145.76:4567/docker/scrapy:latest

MAINTAINER edgar.li "1045909037@qq.com"

COPY . /srv/crawl

#HEALTHCHECK --interval=5s --timeout=3s \
#  CMD curl --fail http://localhost:6080/ || exit 1
