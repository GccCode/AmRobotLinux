#!/usr/bin/env python
# -*- coding:utf-8 -*-

import amazonglobal
from amazondata import AmazonData


class SqlMgr():
    def __init__(self, country):
        self.country = country
        self.ad_sale_task = AmazonData(country)
        self.ad_sale_data = AmazonData(country)
        self.ad_node_info = AmazonData(country)
        self.ad_ip_info = AmazonData(country)
        self.ad_token = AmazonData(country)
        self.ad_rank_task = AmazonData(country)
        self.ad_rank_data = AmazonData(country)
        self.ad_amkiller = AmazonData(country)

        self.db_name_sale_task = ''
        self.db_name_token = ''
        self.db_name_rank_task = ''
        self.db_name_rank_data = ''
        self.db_name_sale_data = ''
        self.db_name_node_info = ''
        self.db_name_ip_info = ''
        self.db_name_amkiller = ''

        self.node_table = ''

        if self.country == 'us':
            self.db_name_sale_task = amazonglobal.db_name_task
            self.db_name_token = amazonglobal.db_name_token
            self.db_name_rank_task = amazonglobal.db_name_rank_task
            self.db_name_rank_data = amazonglobal.db_name_rank_data_us
            self.db_name_sale_data = amazonglobal.db_name_data_us
            self.db_name_node_info = amazonglobal.db_name_node_info_us
            self.db_name_ip_info = amazonglobal.db_name_ip_info_us
            self.db_name_amkiller = amazonglobal.db_name_amkiller_us
        elif self.country == 'jp':
            self.db_name_sale_task = amazonglobal.db_name_task
            self.db_name_token = amazonglobal.db_name_token
            self.db_name_rank_task = amazonglobal.db_name_rank_task
            self.db_name_rank_data = amazonglobal.db_name_rank_data_jp
            self.db_name_sale_data = amazonglobal.db_name_data_jp
            self.db_name_node_info = amazonglobal.db_name_node_info_jp
            self.db_name_ip_info = amazonglobal.db_name_ip_info_jp
            self.db_name_amkiller = amazonglobal.db_name_amkiller_jp

    def set_current_table(self, node_table):
        self.node_table = node_table

    def start(self):
        status = self.ad_sale_task.create_database(self.db_name_sale_task)
        if status == False:
            print("Create Database In Failure + " + self.db_name_sale_task, flush=True)
        else:
            status = self.ad_sale_task.connect_database(self.db_name_sale_task)
            if status == False:
                return False

        status = self.ad_sale_data.create_database(self.db_name_sale_data)
        if status == False:
            print("Create Database In Failure + " + self.db_name_sale_data, flush=True)
        else:
            status = self.ad_sale_data.connect_database(self.db_name_sale_data)
            if status == False:
                return False

        status = self.ad_ip_info.create_database(self.db_name_ip_info)
        if status == False:
            print("Create Database In Failure + " + self.db_name_ip_info, flush=True)
        else:
            status = self.ad_ip_info.connect_database(self.db_name_ip_info)
            if status == False:
                return False

        status = self.ad_node_info.create_database(self.db_name_node_info)
        if status == False:
            print("Create Database In Failure + " + self.db_name_node_info, flush=True)
        else:
            status = self.ad_node_info.connect_database(self.db_name_node_info)
            if status == False:
                return False

        status = self.ad_token.create_database(self.db_name_token)
        if status == False:
            print("Create Database In Failure + " + self.db_name_token, flush=True)
        else:
            status = self.ad_token.connect_database(self.db_name_token)
            if status == False:
                return False

        status = self.ad_rank_task.create_database(self.db_name_rank_task)
        if status == False:
            print("Create Database In Failure + " + self.db_name_rank_task, flush=True)
        else:
            status = self.ad_rank_task.connect_database(self.db_name_rank_task)
            if status == False:
                return False

        status = self.ad_rank_data.create_database(self.db_name_rank_data)
        if status == False:
            print("Create Database In Failure + " + self.db_name_rank_data, flush=True)
        else:
            status = self.ad_rank_data.connect_database(self.db_name_rank_data)
            if status == False:
                return False

        status = self.ad_amkiller.create_database(self.db_name_amkiller)
        if status == False:
            print("Create Database In Failure + " + self.db_name_amkiller, flush=True)
        else:
            status = self.ad_amkiller.connect_database(self.db_name_amkiller)
            if status == False:
                return False

        return True

    def stop(self):
        self.ad_sale_task.disconnect_database()
        self.ad_sale_data.disconnect_database()
        self.ad_ip_info.disconnect_database()
        self.ad_node_info.disconnect_database()
        self.ad_token.disconnect_database()
        self.ad_rank_task.disconnect_database()
        self.ad_rank_data.disconnect_database()
        self.ad_amkiller.disconnect_database()
