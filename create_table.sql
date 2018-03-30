CREATE TABLE `house` (
  `rent_mode` varchar(45) DEFAULT NULL,
  `fangyuan_url` varchar(256) NOT NULL,
  `address` varchar(256) DEFAULT NULL,
  `spec` varchar(90) DEFAULT NULL,
  `contact` varchar(40) DEFAULT NULL,
  `detail` varchar(500) DEFAULT NULL,
  UNIQUE KEY `fangyuan_url` (`fangyuan_url`),
  CONSTRAINT `fk_referer` FOREIGN KEY (`fangyuan_url`) REFERENCES `resource` (`fangyuan_url`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `resource` (
  `address` varchar(256) DEFAULT NULL,
  `fangyuan_url` varchar(256) NOT NULL,
  `img_src` varchar(256) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`fangyuan_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
