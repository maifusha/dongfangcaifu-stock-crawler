> 东方财富股票数据的爬虫.

#### Badages
```
[![build status](https://git.yoursite.com/crawler/stock_crawler/badges/master/build.svg)](https://git.yoursite.com/crawler/stock_crawler/commits/master)
```

#### 本项目爬虫设计
包含以下组件：
* 启动爬虫的Cron定时配置文件
* 若干爬虫蜘蛛（每个蜘蛛对应爬取一套数据）

#### 初次启动本地开发环境执行以下步骤
1. 拷贝`.env.example`至`.env`
2. 拷贝`docker-compose.example.yml`至`docker-compose.yml`
3. 执行`docker login git.yoursite.com:5005`使用`Gitlab`账号登录项目私有`docker`镜像仓库`Container Registry`
4. 运行`docker-compose pull && docker-compose up -d`启动本地开发环境
5. 配置数据表
6. 关闭环境请运行`docker-compose down`

#### 日常开发工作
1. 执行`docker-compose up -d`启动本地开发环境
2. 执行`docker exec -it stock_crawler sh`进入容器使用其提供的`Scrapy`环境调试（退出容器请按键`CTRL + d`）
3. 在宿主机环境下提交代码
4. 关闭环境请运行`docker-compose down`


#### 数据表
```sql
-- mysql容器首次启动会回自动创建数据库 --

ALTER DATABASE `crawler` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

CREATE TABLE `stocks` (
    `code` CHAR(6) NOT NULL COMMENT '股票代码',
    `exchange` CHAR(2) NOT NULL COMMENT '交易所代码',
    `company_name` VARCHAR(32) NOT NULL COMMENT '公司名称',
    `industry_sector_num` CHAR(12) NULL DEFAULT NULL COMMENT '行业代码',
    `launch_date` DATE NULL DEFAULT NULL COMMENT '发行日期',
    `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`code`)
)
COMMENT='股票名单'
DEFAULT CHARSET utf8 COLLATE utf8_general_ci
ENGINE=InnoDB
;

CREATE TABLE `stock_details` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `code` CHAR(6) NOT NULL COMMENT '股票代码',
    `date` DATE NOT NULL COMMENT '行情日期',
    `close_price` FLOAT NULL DEFAULT '0' COMMENT '收盘价',
    `turnover_ratio` FLOAT NULL DEFAULT '0' COMMENT '换手率',
    `pe_ratio` FLOAT NULL DEFAULT '0' COMMENT '市盈率',
    `pb_ratio` FLOAT NULL DEFAULT '0' COMMENT '市净率',
    `total_market_capitalisation` BIGINT UNSIGNED NULL DEFAULT '0' COMMENT '总股本',
    `circulation_market_capitalisation` BIGINT UNSIGNED NULL DEFAULT '0' COMMENT '流通市值',
    `status` SMALLINT NULL DEFAULT '0' COMMENT '股票状态',
    `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='股票行情'
DEFAULT CHARSET utf8 COLLATE utf8_general_ci
ENGINE=InnoDB
;

CREATE TABLE `circulation_shareholders` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `code` CHAR(6) NOT NULL COMMENT '股票代码',
    `data` DATE NOT NULL COMMENT '股东日期',
    `index` SMALLINT UNSIGNED NOT NULL COMMENT '股东排位',
    `name` VARCHAR(256) NULL DEFAULT NULL COMMENT '股东姓名',
    `nature` VARCHAR(32) NULL DEFAULT NULL COMMENT '股东属性',
    `share_num` BIGINT UNSIGNED NOT NULL COMMENT '持股数',
    `share_ratio` FLOAT UNSIGNED NOT NULL COMMENT '持股占比',
    `share_change` BIGINT UNSIGNED NOT NULL COMMENT '持股变动',
    `share_change_ratio` FLOAT UNSIGNED NOT NULL COMMENT '持股变率',
    `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)
COMMENT='十大流通股东'
DEFAULT CHARSET utf8 COLLATE utf8_general_ci
ENGINE=InnoDB
;
```
