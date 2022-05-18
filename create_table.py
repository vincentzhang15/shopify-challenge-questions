#import sys

import mysql.connector
import dbconn


mydb = dbconn()
print(mydb) 

mycursor = mydb.cursor()

doit = 1
if doit:
    mycursor.execute(
        """
        create table `bdiInventoryItems` (
        `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
        `name` varchar(100) not null,
        `category` varchar(100) not null,
        `price` decimal(10,2) not null,
        `amount` MEDIUMINT not null,
        `state` SMALLINT not null default 0,
        `warehouse_location_id` MEDIUMINT not null default 0,
        `comment` varchar(100) not null default '',
        `date_created` datetime default current_timestamp, 
        `last_updated` datetime default current_timestamp,
        primary key(`id`)) engine=InnoDB default charset=utf8mb4;
        """
        )

# sys.exit()

