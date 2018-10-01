#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import sys
import copy
from datetime import date
from datetime import timedelta
from amazondata import AmazonData
from amspider import AmazonSpider
import utils
import io


def get_task_nodes(task_id):
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
            status = amazondata.create_task_table('SALE_TASK')
            if status == False:
                print("Create Table In Failure + SALE_TASK", flush=True)
            else:
                sql = 'select * from SALE_TASK where task_id=' + task_id
                cursor = amazondata.select_data(sql)
                if cursor == False:
                    # print("Get Task Asin In Failure", flush=True)
                    status = False
                else:
                    status = cursor # node, task_id, last_date

            amazondata.disconnect_database()
    return status

def update_task_node(node):
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

def update_asin_status_err(am, node, asin):
    condition = 'asin=\'' + asin + '\''
    return am.update_data(node + '_BS', 'status', '\'err\'', condition)

def is_all_task_finish(task_id):
    amazontask_db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(amazontask_db_name)
    if status == False:
        print("Connect Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        sql = 'select * from SALE_TASK where task_id=\'' + task_id +'\' and last_date <> ' + value
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status

def is_task_finish(node):
    amazontask_db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(amazontask_db_name)
    if status == False:
        print("Connect Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        sql = 'select * from SALE_TASK where node=' + node + ' and last_date <> ' + value
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status

def is_all_inventory_finish(node_table):
    amazontask_db_name = 'amazondata'
    amazondata = AmazonData()
    status = amazondata.connect_database(amazontask_db_name)
    if status == False:
        print("Connect Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        sql = 'select * from ' + node_table + ' where limited=\'no\' and status=\'ok\'' + ' and inventory_date <> ' + value
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status


def get_asin_rows_from_node(ad, table):
    status = False
    sql = 'select * from ' + table + ' where status=\'ok\' and limited=\'no\'' + ' and node=' + node
    cursor = amazondata.select_data(sql)
    if cursor == False:
        print("Get Asin_Rows From Node In Failure" + table, flush=True)
        status = False
    else:
        status = cursor

    return status

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    task_id = sys.argv[1]   # 1
    node_type = sys.argv[2] # BS - NR
    amazonspider = AmazonSpider()
    amazondata = AmazonData()
    status = amazondata.connect_database('amazondata')
    if status == True:
        node_cursor = get_task_nodes(task_id)
        if node_cursor != False:
            while is_all_task_finish(task_id) == False:
                task_info_array_len = node_cursor.rowcount
                task_info_array = node_cursor.fetchall()
                broswer_created = False
                for node_index in range(0, task_info_array_len):
                    try:
                        if node_index >= len(task_info_array):
                            print("asin_index out of limit..", flush=True)
                        task_info = task_info_array[node_index]
                        node = task_info[0]
                        node_table = node + '_' + node_type
                        while is_task_finish(node) == False:
                            while is_all_inventory_finish(node_table) == False:
                                asin_cursor = get_asin_rows_from_node(amazondata, node_table)
                                if asin_cursor != False:
                                    asin_info_array_len = asin_cursor.rowcount
                                    asin_info_array = asin_cursor.fetchall()
                                    print("asin_info_array_len is " + str(len(asin_info_array)), flush=True)
                                    for asin_index in range(0, asin_info_array_len):
                                        if asin_index >= len(asin_info_array):
                                            print("asin_index out of limit.. + " + str(asin_index) + ' ' + str(asin_info_array_len), flush=True)
                                            exit(-1)
                                        asin_info = asin_info_array[asin_index]
                                        asin = asin_info[1]
                                        if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")) and asin_info[8] == 1:
                                            chrome_options = webdriver.ChromeOptions()
                                            prefs = {
                                                'profile.default_content_setting_values': {
                                                    'images': 2,
                                                    'javascript': 2
                                                }
                                            }
                                            chrome_options.add_experimental_option("prefs", prefs)
                                            host_port = utils.getrandomline("myproxy.txt")
                                            print("proxy ip is: " + host_port, flush=True)
                                            proxy_socks_argument = '--proxy-server=socks5://' + host_port
                                            chrome_options.add_argument(proxy_socks_argument)
                                            driver = webdriver.Chrome(chrome_options=chrome_options)
                                            driver.set_page_load_timeout(60)
                                            driver.set_script_timeout(60)
                                            broswer_created = True
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
                                                        if status != -999:
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
                                                                    if avg_sale != -999:
                                                                        status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                                        if status == False:
                                                                            print("avg_sale update fail.. + " + node_table, flush=True)
                                                                        # else:
                                                                        #     print("avg_sale update successfully.. + " + node_table, flush=True)
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
                                                status = update_asin_status_err(amazondata, node, asin)
                                                if status == False:
                                                    print("update asin status faild.. + " + node + ' ' + asin, flush=True)

                            status = update_task_node(node)
                            if status == False:
                                print("update task node faild.. + " + node, flush=True)
                            # else:
                            #     print("update task node sucessfully.. + " + node, flush=True)
                    except Exception as e:
                        print(str(e))
                    finally:
                        if broswer_created == True:
                            driver.quit()
                            broswer_created = False

        amazondata.disconnect_database()
    else:
        print("Connect Database In Failure", flush=True)
