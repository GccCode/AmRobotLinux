#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonsql import AmazonSql
from datetime import *


class AmazonData():
    def __init__(self):
        self.amsql = AmazonSql("login.info")
        self.db = None

    def create_database(self, db_name):
        status = True
        db = self.amsql.connect_sql(False)
        if db == False:
            status = False
        else:
            if self.amsql.is_mysql_database_exsist(db, db_name) == False:
                status = self.amsql.create_db(db, db_name)
            # else:
            #     print("AmazonData Database exsist + " + db_name, flush=True)
            self.amsql.disconnect(db)
        return status

    def connect_database(self, db_name):
        status = True
        db = self.amsql.connect_sql(db_name)
        if db == False:
            status = False
        else:
            self.db = db

        return status

    def disconnect_database(self):
        self.amsql.disconnect(self.db)

    def is_asin_info_table_exsist(self, table):
        return self.amsql.is_mysql_table_exsist(self.db, table)

    def is_table_exsist(self, table):
        return self.amsql.is_mysql_table_exsist(self.db, table)

    def create_ip_table(self, table):
        columns = 'ip VARCHAR(30) NOT NULL, status VARCHAR(2) NOT NULL, PRIMARY KEY (ip)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_rank_task_table(self, table):
        columns = 'id int(8) not null primary key auto_increment, name varchar(30) not null, asin char(10) not null, keyword varchar(50) not null, type char(10) not null, last_date date not null, status char(3) not null'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_task_delete_table(self, table):
        columns = 'node varchar(50) not null, PRIMARY KEY(node)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_ip_info_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def insert_rank_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def create_amkiller_keyword_table(self, table):
        columns = 'date DATE NOT NULL, PRIMARY KEY(date)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_rank_keyword_table(self, table):
        columns = 'keyword VARCHAR(50) NOT NULL, type CHAR(10) NOT NULL, PRIMARY KEY(keyword)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_amkiller_keyword_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def insert_rank_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def create_token_table(self, table):
        columns = 'count int(20) NOT NULL, PRIMARY KEY (count)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_task_status_table(self, table):
        columns = 'status CHAR(5) NOT NULL DEFAULT \'run\' check(status in(\'run\', \'stop\'), PRIMARY KEY (status)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_task_table(self, table):
        columns = 'node VARCHAR(50) NOT NULL, status CHAR(3) NOT NULL, last_date DATE NOT NULL, node_name VARCHAR(100) NOT NULL, PRIMARY KEY (node)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def create_node_info_table(self, table):
        columns = 'node VARCHAR(50) NOT NULL, name CHAR(150) NOT NULL, PRIMARY KEY (node)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_node_info_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def insert_task_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def create_node_table(self, table): # table_name format: node+'node'
        # columns = 'node VARCHAR(11) NOT NULL, name VARCHAR(160) NOT NULL, date DATE NOT NULL, PRIMARY KEY (node)'
        columns = 'rank INT NOT NULL, asin CHAR(10) NOT NULL, node VARCHAR(50) NOT NULL, price FLOAT NOT NULL, review INT NOT NULL, rate FLOAT(2,1) NOT NULL, qa INT NOT NULL, shipping CHAR(3) NOT NULL, seller INT NOT NULL, avg_sale INT NOT NULL, inventory_date DATE NOT NULL, limited VARCHAR(3) NOT NULL, img_url VARCHAR(50) NOT NULL, status VARCHAR(3) NOT NULL, PRIMARY KEY (rank)'
        status = True
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def update_data(self, table, key, value, condition):
        return self.amsql.update_data(self.db, table, key, value, condition)

    def update_data_autoinc(self, table, key, condition):
        return self.amsql.update_data_autoinc(self.db, table, key, condition)

    def update_data_autodes(self, table, key, condition):
        return self.amsql.update_data_autodes(self.db, table, key, condition)

    def add_keyword_column(self, db_name, table, asin, column):
        status = True
        if self.amsql.is_mysql_column_exsit(self.db, db_name, table, asin) == False:
            status = self.amsql.add_column(self.db, table, column)

        return status

    def add_rank_column(self, db_name, table, date, date_column):
        status = True
        if self.amsql.is_mysql_column_exsit(self.db, db_name, table, date) == False:
            status = self.amsql.add_column(self.db, table, date_column)

        return status

    def add_column(self, db_name, table, column_name, column):
        status = True
        if self.amsql.is_mysql_column_exsit(self.db, db_name, table, column_name) == False:
            status = self.amsql.add_column(self.db, table, column)

        return status

    def delete_column(self, db_name, table, column_name):
        status = True
        if self.amsql.is_mysql_column_exsit(self.db, db_name, table, column_name):
            status = self.amsql.delete_column(self.db, table, column_name)

        return status

    def select_data(self, sql):
        return  self.amsql.select_data(self.db, sql)

    def insert_node_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)

    def create_asin_info_table(self, table): #table_name format: node + '-' + type +'-' + asin + '-' + 'info'
        status = True
        columns = 'rank INT NOT NULL, asin CHAR(10) NOT NULL, node VARCHAR(50) NOT NULL, price float NOT NULL, review INT NOT NULL, rate FLOAT(2,1) NOT NULL, qa INT NOT NULL, shipping CHAR(3) NOT NULL, seller INT NOT NULL, avg_sale INT NOT NULL, inventory_date DATE NOT NULL, limited VARCHAR(3) NOT NULL, img_url VARCHAR(20) NOT NULL, status VARCHAR(3) NOT NULL, PRIMARY KEY (rank)'
        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_asin_info_data(self, table, data):
        return self.amsql.insert_data(self.db, table, data)


    def create_inventory_table(self, table): # table_name format: asin + '-inventory'
        status = True
        columns = 'date DATE NOT NULL, inventory INT NOT NULL, PRIMARY KEY (date)'

        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_inventory_data(self, table, data):
        # data = {
        #     'date' : '2018-09-01',
        #     'inventory' : 10
        # }
        return self.amsql.insert_data(self.db, table, data)

    def create_sale_table(self, table): # table_name format: asin + '-sale'
        status = True
        columns = 'date DATE NOT NULL, sale INT NOT NULL, PRIMARY KEY (date)'

        if self.amsql.is_mysql_table_exsist(self.db, table) == False:
            status = self.amsql.create_table(self.db, table, columns)

        return status

    def insert_sale_data(self, table, data):
        # data = {
        #     'date' : '2018-09-01',
        #     'sale' : 10
        # }
        return self.amsql.insert_data(self.db, table, data)

    def query(self, sql):
        return self.amsql.query(self.db, sql)

    def get_yesterday_sale(self, table):
        today = date.today()
        yesterday = date.today() + timedelta(days = -1)
        sql = 'select * from ' + table + ' where date=\'' + yesterday.strftime("%Y-%m-%d") + '\''
        status = self.amsql.select_data(self.db, sql)
        if status == False:
            # print("Get yesterday sale fail...", flush=True)
            return 0

        inventory = status.fetchall()
        yesterday_inventory = inventory[0][1]

        sql = 'select * from ' + table + ' where date=\'' + today.strftime("%Y-%m-%d") + '\''
        status = self.amsql.select_data(self.db, sql)
        if status == False:
            # print("Get today sale fail...", flush=True)
            return 0

        inventory = status.fetchall()
        today_inventory = inventory[0][1]

        yesterday_sale =  yesterday_inventory - today_inventory
        if yesterday_sale < 0:
            yesterday_sale = 0

        return yesterday_sale

    def get_yesterday_inventory(self, table):
        today = date.today()
        yesterday = date.today() + timedelta(days = -1)
        sql = 'select * from ' + table + ' where date=\'' + yesterday.strftime("%Y-%m-%d") + '\''
        status = self.amsql.select_data(self.db, sql)
        if status == False:
            return False

        inventory = status.fetchall()
        yesterday_inventory = inventory[0][1]
        if yesterday_inventory >= 0:
            return yesterday_inventory
        else:
            return False

    def get_column_avg(self, table, column):
        status = -999
        sql = 'select avg(' + column + ') from ' + table
        cursor = self.amsql.query(self.db, sql)
        if cursor != False:
            avg_rows = cursor.fetchall()
            status = avg_rows[0][0]
            if status < 0:
                status = 0

        return status


if __name__ == "__main__":
    amazondata = AmazonData()
    status = amazondata.create_database('amazondata')
    if status == False:
        print("create database fail...", flush=True)
    else:
        print("create database ok...", flush=True)
    status = amazondata.connect_database('amazondata')
    if status == False:
        print("connect to amazondata database fail..", flush=True)
    else:
        print("connect to default database ok..", flush=True)
        amazondata.disconnect_database()

    # status = amazondata.update_data('2285178051_bs_B07GP8QY8H', 'avg_sale', '30', 'asin=\'B07D8LJ9F2\'')
    # if status == False:
    #     print("xxx")
    # else:
    #     print("uuu")
    # status = amazondata.create_database(amazondata.db, 'amazondata')
    # if status == False:
    #     print("create amazondata database fail..", flush=True)
    # else:
    #     print("create amazondata database ok..", flush=True)

    # status = amazondata.create_asin_info_table('2285178051_bs_B07GP8QY8H')
    # if status == False:
    #     print("Create table fail", flush=True)
    # else:
    #     data = {"rank": 7, "asin": "B07D8LJ9F2", "node": "2285178051", "price": 740, "review": 2, "rate": 1.0, "qa": 1, "shipping": "FBM", "seller": 1, "avg_sale": 0, "limited": "no", "img_url": "4124d4tNQbL", "status": "ok"}
    #     status = amazondata.insert_asin_info_data('2285178051_bs_B07GP8QY8H', data)
    #     if status == False:
    #         print("Data Insert fail", flush=True)
    #     else:
    #         print("Data Insert ok")
    # status = amazondata.create_inventory_table('inventory_B07D8LJ9F2')
    # if status == False:
    #     print("fail")
    # else:
    #     print("ok")
    # today = date.today()
    # yesterday = today + timedelta(days=-1)
    # today_data = {
    #     'date': today,
    #     'inventory': 9
    # }
    # status = amazondata.insert_inventory_data('inventory_B07D8LJ9F2', today_data)
    # if status == False:
    #     print("fail1")
    # else:
    #     print("ok1")
    # yesterday_data = {
    #     'date' : yesterday,
    #     'inventory': 30
    # }
    # status = amazondata.insert_inventory_data('inventory_B07DPP7V2M', yesterday_data)
    # if status == False:
    #     print("fail2")
    # else:
    #     print("ok2")
    #
    # status = amazondata.get_yesterday_sale('inventory_B07DPP7V2M')
    # if status == -1:
    #     print("fail3")
    # else:
    #     print("today sale is " + str(status))

    amazondata.disconnect_database()