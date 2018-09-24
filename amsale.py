#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import re
import time
import json
import sys
import io
from selenium.webdriver.common.by import By
from amazonasinpage import AmazonAsinPage
from selenium.common.exceptions import NoSuchElementException
from amazonpage import AmazonPage
import copy
from datetime import date
from datetime import datetime
from datetime import timedelta
from amazondata import AmazonData
from amspider import AmazonSpider
from amazonsql import AmazonSql



def get_task_nodes(task_id):
    status = True
    amazontask_db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.create_database(amazontask_db_name)
    if status == False:
        print("Create Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        status = amazondata.connect_database(amazontask_db_name)
        if status == False:
            print("Connect Database In Failure + " + amazontask_db_name, flush=True)
            status = False
        else:
            sql = 'select * from SALE_TASK where task_id=' + task_id
            cursor = amazondata.select_data(sql)
            if cursor == False:
                print("Get Task Asin In Failure", flush=True)
                status = False
            else:
                status = cursor # node, task_id, last_date

            amazondata.disconnect_database()
    return status

def update_task_node(node):
    status = True
    amazontask_db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(amazontask_db_name)
    if status == False:
        print("Connect Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        condition = 'node=\'' + node + '\''
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        status = amazondata.update_data('SALE_TASK', 'last_date', value, condition)

        amazondata.disconnect_database()

    return status

def get_asin_rows_from_node(ad, table):
    status = True
    sql = 'select * from ' + table + ' where status=\'ok\' and limited=\'no\'' + ' and node=' + node
    cursor = amazondata.select_data(sql)
    if cursor == False:
        print("Get Asin_Rows From Node In Failure" + table, flush=True)
        status = False
    else:
        status = cursor

    return status

if __name__ == "__main__":
    task_id = sys.argv[1]   # 1
    node_type = sys.argv[2] # BS - NR
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {
    #     'profile.default_content_setting_values': {
    #         'images': 2,
    #         'javascript': 2
    #     }
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.set_page_load_timeout(60)
    # driver.set_script_timeout(60)
    amazonspider = AmazonSpider()
    amazondata = AmazonData()
    status = amazondata.connect_database('amazondata')
    if status == True:
        node_cursor = get_task_nodes(task_id)
        if node_cursor == True:
            task_info_array_len = node_cursor.rowcount
            task_info_array = node_cursor.fetchall()
            for node_index in range(0, task_info_array_len):
                driver = None
                try:
                    chrome_options = webdriver.ChromeOptions()
                    prefs = {
                        'profile.default_content_setting_values': {
                            'images': 2,
                            'javascript': 2
                        }
                    }
                    chrome_options.add_experimental_option("prefs", prefs)
                    driver = webdriver.Chrome(chrome_options=chrome_options)
                    driver.set_page_load_timeout(60)
                    driver.set_script_timeout(60)
                    task_info = task_info_array[node_index]
                    node = task_info['node']
                    node_table = node + '_BS'
                    asin_cursor = get_asin_rows_from_node(amazondata, node_table)
                    if asin_cursor == True:
                        asin_info_array_len = asin_cursor.rowcount
                        asin_info_array = asin_cursor.fetchall()
                        for asin_index in range(0, asin_info_array_len):
                            asin_info = asin_info_array[asin_index]
                            asin = asin_info['asin']
                            result = amazonspider.get_inventory_jp(driver, asin)
                            if result != False:
                                cur_date = date.today()
                                data = {
                                    'date': cur_date,
                                    'inventory': result['inventory']
                                }
                                inventory_table = 'INVENTORY_' + asin
                                status = amazondata.insert_inventory_data(inventory_table, data)
                                if status == True:
                                    condition = 'asin=\'' + asin + '\''
                                    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                    status = amazondata.update_data(node_table, 'inventory_date', value, condition)
                                    if status == True:
                                        status = amazondata.get_yesterday_sale(inventory_table)
                                        if status != False:
                                            yesterday = date.today() + timedelta(days=-1)
                                            data = {
                                                'date': yesterday,
                                                'sale': copy.deepcopy(status)
                                            }
                                            sale_table = 'SALE_' + asin
                                            status = amazondata.create_sale_table(sale_table)
                                            if status == True:
                                                status = amazondata.insert_sale_data(sale_table, data)
                                                if status == True:
                                                    avg_sale = amazondata.get_column_avg(sale_table, 'sale')
                                                    if avg_sale != -1:
                                                        status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                        if status == False:
                                                            print("avg_sale update fail.. + " + node_table, flush=True)
                                                        else:
                                                            print("avg_sale update successfully.. + " + node_table, flush=True)
                                                        status = update_task_node(node)
                                                        if status == False:
                                                            print("update task node faild.. + " + node, flush=True)
                                                        else:
                                                            print("update task node sucessfully.. + " + node, flush=True)
                                                    else:
                                                        print(" get avg_sale fail.. + " + node_table, flush=True)
                                                else:
                                                    print("sale_data insert fail... + " + sale_table, flush=True)
                                            else:
                                                print("sale_table create fail.. + " + sale_table, flush=True)
                                        else:
                                            print("get_yesterday_sale fail.. + " + inventory_table, flush=True)
                                    else:
                                        print("invetory_date update fail.. + " + node_table, flush=True)
                                else:
                                    print("inventory data insert fail.. + " + inventory_table, flush=True)
                            else:
                                print("Get Inventory Jp In Failure.", flush=True)
                    else:
                        pass
                except Exception as e:
                    print(str(e))
                finally:
                    driver.quit()
        else:
            print("get task node fail + " + task_id, flush=True)

        amazondata.disconnect_database()
    else:
        print("Connect Database In Failure", flush=True)
