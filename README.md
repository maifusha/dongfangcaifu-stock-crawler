> 仓位在线项目相关数据的爬虫

[![build status](https://git.maifusha.com/crawler/cangweizaixian_crawl/badges/master/build.svg)](https://git.maifusha.com/crawler/cangweizaixian_crawl)


#### 注意事项
* 一个完整的爬虫项目设计为包含以下组件
  1. 启动爬虫的Cron定时配置文件
  2. 若干蜘蛛
* 一个网站包含多个蜘蛛， 一个蜘蛛对应爬取一套数据
* 爬虫部署请在**蜘蛛空闲时段**发布


#### 初次启动本地开发环境执行以下步骤
1. 拷贝`.env.example`至`.env`
2. 拷贝`docker-compose.example.yml`至`docker-compose.yml`
3. 执行`docker login git.maifusha.com:5005`使用`Gitlab`账号登录项目私有`docker`镜像仓库`Container Registry`
4. 运行`docker-compose pull && docker-compose up -d`启动环境
5. 确保已配置好仓位在线公众号项目中的数据库
6. 执行`docker exec cangweizaixian_crawl scrapy startproject crawl /srv/crawl`初始化项目爬虫
7. 关闭环境请运行`docker-compose down`


#### 日常开发工作
1. 执行`docker-compose up -d`启动本地开发环境
2. 执行`docker exec -it cangweizaixian_crawl sh`进入容器使用其提供的`Scrapy & PyMySQL`环境（退出容器请按键`CTRL + d`）

```
    scrapy genspider --template basic 蜘蛛名字 爬取地址  #为项目爬虫新增基本蜘蛛
    
    . . .  #开发蜘蛛逻辑
    scrapy shell 爬取地址  #进入ScrapyShell进行调试
    
    scrapy crawl 蜘蛛名字  #启动蜘蛛测试爬取
```

3. 在宿主机环境下`git`命令行提交代码
4. 关闭环境请运行`docker-compose down`
