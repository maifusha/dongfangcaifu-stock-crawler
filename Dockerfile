FROM git.yoursite.com:5005/docker/scrapy:latest

LABEL maintainer="lixin <1045909037@qq.com>"

COPY . /srv/crawl

COPY crontab /etc/crontabs/root

ENTRYPOINT ["crond", "-L", "/var/log/crond.log"]
CMD ["tail", "-f", "/var/log/crond.log"]

#HEALTHCHECK --interval=5s --timeout=3s \
#  CMD curl --fail http://localhost:6080/ || exit 1
