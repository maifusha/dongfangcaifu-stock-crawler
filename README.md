> 股票数据的爬虫

[![build status](https://git.maifusha.com/crawler/stock_crawler/badges/master/build.svg)](https://git.maifusha.com/crawler/stock_crawler/commits/master)


#### 注意事项
* 该项目设计为包含以下组件
  1. 启动爬虫的Cron定时配置文件
  2. 若干爬虫蜘蛛（每个蜘蛛对应爬取一套数据）
* 项目起步需要初始化爬虫`docker exec stock_crawler scrapy startproject crawl /srv/crawl`
* 爬虫部署请在**蜘蛛空闲时段**发布


#### 初次启动本地开发环境执行以下步骤
1. 拷贝`.env.example`至`.env`
2. 拷贝`docker-compose.example.yml`至`docker-compose.yml`
3. 执行`docker login git.maifusha.com:5005`使用`Gitlab`账号登录项目私有`docker`镜像仓库`Container Registry`
4. 运行`docker-compose pull && docker-compose up -d`启动本地开发环境
5. 确保已初始化好关联数据库
6. 关闭环境请运行`docker-compose down`


#### 日常开发工作
1. 执行`docker-compose up -d`启动本地开发环境
2. 执行`docker exec -it stock_crawler sh`进入容器使用其提供的`Scrapy`环境（退出容器请按键`CTRL + d`）

```
scrapy genspider [--template basic] 爬虫蜘蛛名字 爬取域名  #为项目爬虫新增基本爬虫蜘蛛，参数--template可选

dosomething  #开发爬虫蜘蛛逻辑

scrapy shell 爬取地址  #进入ScrapyShell进行调试

scrapy crawl 爬虫蜘蛛名字  #启动爬虫蜘蛛测试爬取
```

3. 在宿主机环境下`git`命令行提交代码
4. 关闭环境请运行`docker-compose down`