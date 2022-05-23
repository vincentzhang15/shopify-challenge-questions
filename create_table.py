#import sys

import mysql.connector
import dbconn


mydb = dbconn.dbconn()
print(mydb) 

mycursor = mydb.cursor()

doit = 0
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


doit = 1
if doit:
    mycursor.execute(
        """
        create table `deitableids` (
        `name` varchar(100) not null,
        `id` BIGINT NOT NULL,
        primary key(`name`)) engine=InnoDB default charset=utf8mb4;
        """
        )

doit = 1
if doit:
    mycursor.execute("drop table if exists `deiimages`")
    mycursor.execute(
        """
        create table `deiimages` (
        `id` BIGINT NOT NULL,
        `name` varchar(100) not null,
        `prop` SMALLINT NOT NULL,
        `content` varchar(50) NOT NULL,
        `userid` varchar(50) NOT NULL,
        `magic` varchar(520) not null,
        `date_created` datetime default current_timestamp, 
        `last_updated` datetime default current_timestamp,
        primary key(`id`)) engine=InnoDB default charset=utf8mb4;
        """
        )

doit = 1
if doit:
    mycursor.execute(
        """
        create table `deitags` (
        `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
        `name` varchar(100) not null,
        primary key(`id`)) engine=InnoDB default charset=utf8mb4;
        """
        )

doit = 1
if doit:
    mycursor.execute(
        """
        create table `deiimagetags` (
        `imageid` BIGINT NOT NULL,
        `tagid` MEDIUMINT NOT NULL,
        primary key(`imageid`, `tagid`)) engine=InnoDB default charset=utf8mb4;
        """
        )


