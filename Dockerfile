FROM 121.40.145.76:4567/docker/scrapy:latest

MAINTAINER edgar.li "1045909037@qq.com"

COPY . /srv/crawl

COPY crontab /etc/crontabs/root

VOLUME ["/var/log/scrapy.log", "/var/log/crond.log"]

ENTRYPOINT ["crond", "-L", "/var/log/crond.log"]
CMD ["tail", "-f", "/var/log/crond.log"]

#HEALTHCHECK --interval=5s --timeout=3s \
#  CMD curl --fail http://localhost:6080/ || exit 1
