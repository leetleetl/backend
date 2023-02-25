USE
holdsql;
DROP TABLE IF EXISTS `hold`;

CREATE TABLE
    `hold`
(
    `code` varchar(9)  NOT NULL COMMENT '股票代码',

    `buyDate` varchar(8) COMMENT '购买日期',

    `buyPrice`  float COMMENT '购买价格',



     PRIMARY KEY (code)

) ENGINE = InnoDB DEFAULT CHARSET=utf8;