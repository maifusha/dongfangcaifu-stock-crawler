> 仓位在线项目相关数据的爬虫

[![build status](https://121.40.145.76:8443/Crawler/cangweizaixian_spider/badges/master/build.svg)](https://121.40.145.76:8443/Crawler/cangweizaixian_spider/commits/master)

#### 初次启动本地开发环境执行以下步骤
1. 拷贝`.env.example`至`.env`
2. 拷贝`docker-compose.example.yml`至`docker-compose.yml`
3. 执行`docker login 121.40.145.76:4567`使用`Gitlab`账号登录项目私有`docker`镜像仓库`Container Registry`
4. 运行`docker-compose pull && docker-compose up -d`启动环境
5. 创建数据库并配置权限 `mysql -h127.0.0.1 -uroot -p`
```sql
      CREATE DATABASE IF NOT EXISTS cangweizaixian DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
      GRANT ALL ON cangweizaixian.* TO cangweizaixian@'%' IDENTIFIED BY '*S.AB#d.OwoPJ~3';
      GRANT ALL ON cangweizaixian.* TO cangweizaixian@'localhost' IDENTIFIED BY '*S.AB#d.OwoPJ~3';
      flush privileges;
```
6. 执行`docker exec cangweizaixian_spider scrapy startproject crawl /srv/crawl`初始化爬虫
7. 关闭环境请运行`docker-compose down`


#### 日常开发工作
1. 执行`docker-compose up -d`启动本地开发环境
2. 执行`docker exec -it cangweizaixian_spider sh`进入容器使用其提供的`Scrapy & PyMySQL`环境（退出容器请按键`CTRL + d`）：
```
scrapy genspider --template basic 蜘蛛名字 爬取地址  #新建蜘蛛
scrapy shell --nolog 爬取地址  #进入ScrapyShell进行调试
scrapy crawl 蜘蛛名字  #启动蜘蛛开始爬取
```
3. 在宿主机环境下`git`命令行提交代码
4. 关闭环境请运行`docker-compose down`
