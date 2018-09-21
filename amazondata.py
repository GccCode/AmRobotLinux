#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonsql import AmazonSql



class AmazonData():
    def __init__(self):
        pass

    def create_node_table(self, table): # table_name format: node+'node'
        rows = 'asin CHAR(10) NOT NULL, name VARCHAR(100) NOT NULL, date DATE NOT NULL, PRIMARY KEY (asin)'
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.create_table(db, table, rows)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def insert_node_data(self, table, data):
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.insert_data(db, table, data)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    # def create_asin_table(self, table): # table_name format: nodenumber+'asin'
    #     rows = 'asin CHAR(10) NOT NULL, node VARCHAR(50) NOT NULL, date DATE NOT NULL, PRIMARY KEY (asin)'
    #     amsql = AmazonSql("login.info")
    #     db = amsql.connect_sql('amazondata')
    #     if db == False:
    #         return False
    #
    #     status = amsql.create_table(db, table, rows)
    #     if status == False:
    #         return False
    #
    #     amsql.disconnect(db)
    #
    #     return True
    #
    # def insert_asin_data(self, table, data):
    #     amsql = AmazonSql("login.info")
    #     db = amsql.connect_sql('amazondata')
    #     if db == False:
    #         return False
    #
    #     status = amsql.insert_data(db, table, data)
    #     if status == False:
    #         return False
    #
    #     amsql.disconnect(db)
    #
    #     return True

    def create_asin_info_table(self, table): #table_name format: node + '-' + type +'-' + asin + '-' + 'info'
        rows = 'rank INT NOT NULL, asin CHAR(10) NOT NULL, node VARCHAR(50) NOT NULL, price INT NOT NULL, \
                review INT NOT NULL, rate FLOAT(2,1) NOT NULL, qa INT NOT NULL, shipping CHAR(3) NOT NULL, seller INT NOT NULL, avg_sale INT NOT NULL, \
                limited VARCHAR(3) NOT NULL, img_url VARCHAR(12) NOT NULL, PRIMARY KEY (rank)'
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.create_table(db, table, rows)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def insert_asin_info_data(self, table, data):
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.insert_data(db, table, data)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def create_inventory_table(self, table): # table_name format: asin + '-inventory'
        rows = 'asin CHAR(10) NOT NULL, PRIMARY KEY (asin)'
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.create_table(db, table, rows)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def insert_inventory_data(self, table, data):
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.insert_data(db, table, data)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def create_sale_table(self, table): # table_name format: asin + '-sale'
        rows = 'asin CHAR(10) NOT NULL, PRIMARY KEY (asin)'
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.create_table(db, table, rows)
        if status == False:
            return False

        amsql.disconnect(db)

        return True

    def insert_sale_data(self, table, data):
        amsql = AmazonSql("login.info")
        db = amsql.connect_sql('amazondata')
        if db == False:
            return False

        status = amsql.insert_data(db, table, data)
        if status == False:
            return False

        amsql.disconnect(db)

        return True