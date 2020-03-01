DROP TABLE IF EXISTS ftx_btc_move;
CREATE TABLE `ftx_btc_move`(
   `id` VARCHAR(100) NOT NULL,
   `liquidation` VARCHAR(100),
   `price` VARCHAR(100),
   `side` VARCHAR(100),
   `size` VARCHAR(100),
   `time` VARCHAR(100),
   `ticker` VARCHAR(100),
   `gmt_create` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;