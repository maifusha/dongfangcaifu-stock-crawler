> 股票数据的爬虫

[![build status](https://git.maifusha.com/crawler/stock_crawler/badges/master/build.svg)](https://git.maifusha.com/crawler/stock_crawler/commits/master)


#### 初次启动本地开发环境执行以下步骤
1. 拷贝`.env.example`至`.env`
2. 拷贝`docker-compose.example.yml`至`docker-compose.yml`
3. 执行`docker login git.maifusha.com:5005`使用`Gitlab`账号登录项目私有`docker`镜像仓库`Container Registry`
4. 运行`docker-compose pull && docker-compose up -d`启动本地开发环境
5. 确保已配置好关联数据库
6. 关闭环境请运行`docker-compose down`


#### 日常开发工作
1. 执行`docker-compose up -d`启动本地开发环境
2. 执行`docker exec -it stock_crawler sh`进入容器使用其提供的`Scrapy`环境调试（退出容器请按键`CTRL + d`）
3. 在宿主机环境下提交代码
4. 关闭环境请运行`docker-compose down`