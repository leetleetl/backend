drop
database if exists `transaction`;
create
database `transaction`;

USE
transaction;

-- 交易
DROP TABLE IF EXISTS `transaction`;

CREATE TABLE
`transaction`
(


    `code`     varchar(9) NOT NULL COMMENT '股票代码',

    `date`     varchar(8) COMMENT '日期',

    `price` float COMMENT '股价' DEFAULT 0.0,

    `kaipan` float COMMENT '主力' DEFAULT 0.0,

    `vol` int COMMENT '持有量' DEFAULT 0,




    PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `codelist1`;
DROP TABLE IF EXISTS `codelist2`;
DROP TABLE IF EXISTS `codelist3`;
#输出表
CREATE TABLE
    `codelist1`
(   `code`     varchar(9) NOT NULL COMMENT '图片筛选后的股票代码',
PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE
    `codelist2`
(   `code`     varchar(9) NOT NULL COMMENT '第一轮后的股票代码',
PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;CREATE TABLE
    `codelist3`
(   `code`     varchar(9) NOT NULL COMMENT '第二轮后的股票代码',
PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `realtime`;

CREATE TABLE
    `realtime`
(


    `code`     varchar(9) NOT NULL COMMENT '股票代码',

    `gujia`     float COMMENT '股价',

    `kaipan`     float COMMENT '开盘价',

    `super` float COMMENT '超大单',

    `zhuli` float COMMENT '主力',

    `fenshiliang` float COMMENT '分时量',

    `fenshiliang2` float COMMENT '分时量',



    PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;DROP TABLE IF EXISTS `hold`;

DROP TABLE IF EXISTS `hold`;

CREATE TABLE
    `hold`
(
    `code` varchar(9)  NOT NULL COMMENT '股票代码',

    `buyDate` varchar(8) COMMENT '购买日期',



     PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `falsecode`;

CREATE TABLE
    `falsecode`
(   `code`     varchar(9) NOT NULL COMMENT '加载失败代码',
PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `buy`;

CREATE TABLE
    `buy`
(
    `traid` varchar(17)  NOT NULL COMMENT 'id',

    `code` varchar(9)  NOT NULL COMMENT '股票代码',

    `buyDate` varchar(8) COMMENT '购买日期',



     PRIMARY KEY (traid)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `sell`;

CREATE TABLE
    `sell`
(
    `traid` varchar(17)  NOT NULL COMMENT 'id',

    `code` varchar(9)  NOT NULL COMMENT '股票代码',

    `buyDate` varchar(8) COMMENT '购买日期',



     PRIMARY KEY (traid)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;

