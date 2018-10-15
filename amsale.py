#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import copy
from datetime import date
from datetime import timedelta
from amazondata import AmazonData
from amspider import AmazonSpider
import amazonwrapper
import io
import time
import traceback
import amazonglobal


def get_task_nodes(db_name, task_id):
    amazontask_db_name = db_name
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
            status = amazondata.create_task_table('sale_task_jp')
            if status == False:
                print("Create Table In Failure + sale_task_jp", flush=True)
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

def update_task_node(db_name, table, node):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("Connect Database In Failure + " + db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        condition = 'node=\'' + node + '\''
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        status = amazondata.update_data(table, 'last_date', value, condition)

        amazondata.disconnect_database()

    return status

def update_asin_status_err(am, node, asin):
    condition = 'asin=\'' + asin + '\''
    return am.update_data(node + '_BS', 'status', '\'err\'', condition)

def is_all_task_finish(task_id):
    amazontask_db_name = amazonglobal.db_name_task
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

def is_token_runout():
    db_name = amazonglobal.db_name_token
    table = amazonglobal.table_token
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("create database in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("Connect Database In Failure + " + db_name, flush=True)
            status = False
        else:
            status = amazondata.create_token_table(table)
            if status == False:
                print("create token table in failure...", flush=True)
            else:
                sql = 'select * from ' + table + ' where count<>0'
                status = amazondata.select_data(sql)
                if status == False:
                    status = True
                else:
                    status = False

            amazondata.disconnect_database()

    return status

def is_task_running():
    db_name = amazonglobal.db_name_task
    table = amazonglobal.table_sale_task_status
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("create database in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("Connect Database In Failure + " + db_name, flush=True)
            status = False
        else:
            status = amazondata.create_task_status_table(table)
            if status == False:
                print("create task status table in failure...", flush=True)
            else:
                sql = 'select * from ' + table + ' where status=\'stop\''
                status = amazondata.select_data(sql)
                if status == False:
                    status = True
                else:
                    status = False

                amazondata.disconnect_database()

    return status

def update_task_status(task_status):
    db_name = amazonglobal.db_name_task
    table = amazonglobal.table_sale_task_status
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("create database in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("Connect Database In Failure + " + db_name, flush=True)
            status = False
        else:
            if task_status == 'stop':
                condition = 'status=\'run\''
            elif task_status == 'run':
                condition = 'status=\'stop\''
            status = amazondata.update_data(table, 'status', '\''+ task_status + '\'', condition)

            amazondata.disconnect_database()

    return status

def update_token_count():
    db_name = amazonglobal.db_name_token
    table = amazonglobal.table_token
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("create database in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("Connect Database In Failure + " + db_name, flush=True)
            status = False
        else:
            condition = 'count=0'
            status = amazondata.update_data(table, 'count', 20, condition)

            amazondata.disconnect_database()

    return status

def desc_token_count():
    db_name = amazonglobal.db_name_token
    table = amazonglobal.table_token
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("create database in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("Connect Database In Failure + " + db_name, flush=True)
            status = False
        else:
            condition = 'count<>0'
            status = amazondata.update_data_autodes(table, 'count', condition)

            amazondata.disconnect_database()

    return status

def is_task_finish(db_name, table, node):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("Connect Database In Failure + " + db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        sql = 'select * from ' + table + ' where node=\'' + node + '\' and last_date <> ' + value
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status

def is_all_inventory_finish(country, node_table):
    if country == 'us':
        data_db_name = amazonglobal.db_name_data_us
    elif country == 'jp':
        data_db_name = amazonglobal.db_name_data_jp
    amazondata = AmazonData()
    status = amazondata.connect_database(data_db_name)
    if status == False:
        print("Connect Database In Failure + " + data_db_name, flush=True)
        status = False
    else:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        if country == 'us':
            sql = 'select * from ' + node_table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>9' + ' and inventory_date <> ' + value
        elif country == 'jp':
            sql = 'select * from ' + node_table + ' where limited=\'no\' and status=\'ok\'' + ' and inventory_date <> ' + value
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status


def get_asin_rows_from_node(ad, country, table):
    status = False
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    if country == 'us':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>9 and inventory_date <> ' + value
    elif country == 'jp':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\'' + ' and inventory_date <> ' + value
    cursor = ad.select_data(sql)
    if cursor == False:
        print("Get Asin_Rows From Node In Failure" + table, flush=True)
        status = False
    else:
        status = cursor

    return status

def amsale_from_mysql(country, node_type):
    ips_array = amazonwrapper.get_all_accessible_ip()
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    task_db = amazonglobal.db_name_task
    amazonspider = AmazonSpider()
    amazondata = AmazonData()
    status = False
    if country == 'us':
        task_table = amazonglobal.table_sale_task_us
        status = amazondata.connect_database(amazonglobal.db_name_data_us)
    elif country == 'jp':
        task_table = amazonglobal.table_sale_task_jp
        status = amazondata.connect_database(amazonglobal.db_name_data_jp)
    if status == True:
        try:
            cur_date = date.today()
            value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
            status_condition = 'status<>\'no\' and last_date<>' + value
            node_task = amazonwrapper.get_one_data(task_db, task_table, status_condition)
            while node_task != False:
                t1 = time.time()
                node = node_task[0]
                node_table = node + '_' + node_type
                sql_condition = 'node=' + '\'' + node + '\''
                # print(node, flush=True)
                # print(node_table, flush=True)
                # print(sql_condition, flush=True)
                status = amazonwrapper.update_data(task_db, task_table, 'status', '\'no\'', sql_condition)
                if status != False:
                    while is_task_finish(task_db, task_table, node) == False:
                        while is_all_inventory_finish(country, node_table) == False:
                            asin_cursor = get_asin_rows_from_node(amazondata, country, node_table)
                            if asin_cursor != False:
                                asin_info_array = asin_cursor.fetchall()
                                asin_info_array_len = len(asin_info_array)
                                for asin_index in range(0, asin_info_array_len):
                                    if asin_index >= len(asin_info_array):
                                        print("asin_index out of limit.. + " + str(asin_index) + ' ' + str(asin_info_array_len), flush=True)
                                        exit(-1)
                                    asin_info = asin_info_array[asin_index]
                                    asin = asin_info[1]
                                    status = False
                                    if country == 'us':
                                        if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")) and asin_info[8] > 0  and asin_info[8] < 4 and asin_info[7] != 'FBM' and float(asin_info[3]) > 9:
                                            status = True
                                    elif country == 'jp':
                                        if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")):
                                            status = True
                                    if status == True:
                                        if country == 'jp':
                                            result = amazonspider.get_inventory_jp(False, asin, ips_array, True)
                                        elif country == 'us':
                                            result = amazonspider.get_inventory_us(False, asin, ips_array, True)
                                        if result != False and result != -111:
                                            cur_date = date.today()
                                            data = {
                                                'date': cur_date,
                                                'inventory': result['inventory']
                                            }
                                            if result['limited'] == 'yes':
                                                condition = 'asin=\'' + asin + '\''
                                                status = amazondata.update_data(node_table, 'limited', '\'yes\'', condition)
                                            else:
                                                inventory_table = 'INVENTORY_' + asin
                                                if amazondata.is_table_exsist(inventory_table) == False:
                                                    status = amazondata.create_inventory_table(inventory_table)
                                                    if status == False:
                                                        print("create invetory table in failure...", flush=True)
                                                status = amazondata.insert_inventory_data(inventory_table, data)
                                                if status == True:
                                                    condition = 'asin=\'' + asin + '\''
                                                    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                                    status = amazondata.update_data(node_table, 'inventory_date',
                                                                                    value, condition)
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
                                                                status = amazondata.insert_sale_data(sale_table,
                                                                                                     data)
                                                                if status == True:
                                                                    avg_sale = amazondata.get_column_avg(sale_table, 'sale')
                                                                    if avg_sale != -999:
                                                                        status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                                        if status == False:
                                                                            print("avg_sale update fail.. + " + node_table, flush=True)
                                                                    else:
                                                                        print(" get avg_sale fail.. + " + node_table, flush=True)
                                                                else:
                                                                    print(
                                                                        "sale_data insert fail... + " + sale_table, flush=True)
                                                            else:
                                                                print("sale_table create fail.. + " + sale_table, flush=True)
                                                    else:
                                                        print("invetory_date update fail.. + " + node_table, flush=True)
                                                else:
                                                    print("inventory data insert fail.. + " + inventory_table, flush=True)
                                        else:
                                            if result == -111:
                                                print("Ip blocking..", flush=True)
                                                ips_array = amazonwrapper.get_all_accessible_ip()
                                                if ips_array == False:
                                                    print("no accessible ip", flush=True)
                                                    exit(-1)
                                                status = False
                                                continue
                                            print("Get Inventory In Failure.", flush=True)
                                            status = update_asin_status_err(amazondata, node, asin)
                                            if status == False:
                                                print("update asin status faild.. + " + node + ' ' + asin, flush=True)

                        if is_all_inventory_finish(country, node_table) == True:
                            status = update_task_node(task_db, task_table, node)
                            if status == False:
                                print("update task node failed.. + " + node, flush=True)

                            status = amazonwrapper.update_data(task_db, task_table, 'status', '\'ok\'', sql_condition)
                            if status != False:
                                print("amsale finish " + node, flush=True)

                t2 = time.time()
                print("总耗时：" + format(t2 - t1))
                node_task = amazonwrapper.get_one_data(task_db, task_table, status_condition)
        except Exception as e:
            print(traceback.format_exc(), flush=True)
            exit()
            amazonwrapper.update_data(task_db, task_table, 'status', '\'ok\'', sql_condition)

        amazondata.disconnect_database()
    else:
        print("Connect Database In Failure", flush=True)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    task = sys.argv[1]
    if task == 'run':
        country = sys.argv[2]
        type = sys.argv[3]
        while is_task_running():
            while is_token_runout() == False:
                status = desc_token_count()
                if status == False:
                    print('desc token count in failure...', flush=True)
                    exit(-1)
                amsale_from_mysql(country, type)
            update_task_status('stop')
    elif task == 'fix':
        while is_task_running() == False:
            country = sys.argv[2]
            status = update_token_count()
            if status == False:
                print('update token count in failure...', flush=True)
            else:
                if country == 'us':
                    amazonwrapper.update_all_task_status(amazonglobal.db_name_task, amazonglobal.table_sale_task_us, country)
                elif country == 'jp':
                    amazonwrapper.update_all_task_status(amazonglobal.db_name_task, amazonglobal.table_sale_task_jp, country)

                time.sleep(60)
    # task_id = sys.argv[1]   # 1
    # node_type = sys.argv[2] # BS - NR
    # country = sys.argv[3] # us/jp
    # t1 = time.time()
    # ips_array = amazonwrapper.get_all_accessible_ip()
    # if ips_array == False:
    #     print("no accessible ip", flush=True)
    #     exit(-1)
    # t2 = time.time()
    # print("总耗时：" + format(t2 - t1))
    # amazonspider = AmazonSpider()
    # amazondata = AmazonData()
    # if country == 'jp':
    #     status = amazondata.connect_database('amazondata')
    # elif country == 'us':
    #     status = amazondata.connect_database('amazondata_us')
    # if status == True:
    #     if country == 'jp':
    #         node_cursor = get_task_nodes('amazontask', task_id)
    #     elif country == 'us':
    #         node_cursor = get_task_nodes('amazontask_us', task_id)
    #     if node_cursor != False:
    #         while is_all_task_finish(task_id) == False:
    #             # task_info_array_len = node_cursor.rowcount
    #             task_info_array = node_cursor.fetchall()
    #             task_info_array_len =  len(task_info_array)
    #             broswer_created = False
    #             driver = False
    #             for node_index in range(0, task_info_array_len):
    #                 try:
    #                     if node_index >= len(task_info_array):
    #                         print("asin_index out of limit..", flush=True)
    #                     task_info = task_info_array[node_index]
    #                     node = task_info[0]
    #                     node_table = node + '_' + node_type
    #                     while is_task_finish('amazontask', 'SALE_TASK', node) == False:
    #                         while  is_all_inventory_finish(node_table) == False:
    #                             asin_cursor = get_asin_rows_from_node(amazondata, node_table)
    #                             if asin_cursor != False:
    #                                 # asin_info_array_len = asin_cursor.rowcount
    #                                 asin_info_array = asin_cursor.fetchall()
    #                                 asin_info_array_len = len(asin_info_array)
    #                                 for asin_index in range(0, asin_info_array_len):
    #                                     if asin_index >= len(asin_info_array):
    #                                         print("asin_index out of limit.. + " + str(asin_index) + ' ' + str(asin_info_array_len), flush=True)
    #                                         exit(-1)
    #                                     asin_info = asin_info_array[asin_index]
    #                                     asin = asin_info[1]
    #                                     if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")) and asin_info[8] == 1:
    #                                         result = amazonspider.get_inventory_jp(driver, asin, ips_array, True)
    #                                         if result != False and result != -111:
    #                                             cur_date = date.today()
    #                                             data = {
    #                                                 'date': cur_date,
    #                                                 'inventory': result['inventory']
    #                                             }
    #                                             if result['limited'] == 'yes':
    #                                                 condition = 'asin=\'' + asin + '\''
    #                                                 status = amazondata.update_data(node_table, 'limited', '\'yes\'', condition)
    #                                             else:
    #                                                 inventory_table = 'INVENTORY_' + asin
    #                                                 status = amazondata.insert_inventory_data(inventory_table, data)
    #                                                 if status == True:
    #                                                     condition = 'asin=\'' + asin + '\''
    #                                                     value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    #                                                     status = amazondata.update_data(node_table, 'inventory_date', value, condition)
    #                                                     if status == True:
    #                                                         status = amazondata.get_yesterday_sale(inventory_table)
    #                                                         if status != -999:
    #                                                             yesterday = date.today() + timedelta(days=-1)
    #                                                             data = {
    #                                                                 'date': yesterday,
    #                                                                 'sale': copy.deepcopy(status)
    #                                                             }
    #                                                             sale_table = 'SALE_' + asin
    #                                                             status = amazondata.create_sale_table(sale_table)
    #                                                             if status == True:
    #                                                                 status = amazondata.insert_sale_data(sale_table, data)
    #                                                                 if status == True:
    #                                                                     avg_sale = amazondata.get_column_avg(sale_table, 'sale')
    #                                                                     if avg_sale != -999:
    #                                                                         status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
    #                                                                         if status == False:
    #                                                                             print("avg_sale update fail.. + " + node_table, flush=True)
    #                                                                         # else:
    #                                                                         #     print("avg_sale update successfully.. + " + node_table, flush=True)
    #                                                                     else:
    #                                                                         print(" get avg_sale fail.. + " + node_table, flush=True)
    #                                                                 else:
    #                                                                     print("sale_data insert fail... + " + sale_table, flush=True)
    #                                                             else:
    #                                                                 print("sale_table create fail.. + " + sale_table, flush=True)
    #                                                     else:
    #                                                         print("invetory_date update fail.. + " + node_table, flush=True)
    #                                                 else:
    #                                                     print("inventory data insert fail.. + " + inventory_table, flush=True)
    #                                         else:
    #                                             if result == -111:
    #                                                 print("Ip blocking..", flush=True)
    #                                                 ips_array = amazonwrapper.get_all_accessible_ip()
    #                                                 if ips_array == False:
    #                                                     print("no accessible ip", flush=True)
    #                                                     exit(-1)
    #                                                 status = False
    #                                                 continue
    #                                             print("Get Inventory Jp In Failure.", flush=True)
    #                                             status = update_asin_status_err(amazondata, node, asin)
    #                                             if status == False:
    #                                                 print("update asin status faild.. + " + node + ' ' + asin, flush=True)
    #
    #                         if is_all_inventory_finish(node_table) == True:
    #                             status = update_task_node('amazontask', 'SALE_TASK', node)
    #                             if status == False:
    #                                 print("update task node faild.. + " + node, flush=True)
    #                         # else:
    #                         #     print("update task node sucessfully.. + " + node, flush=True)
    #                 except Exception as e:
    #                     print(str(e))
    #                 finally:
    #                     if broswer_created == True:
    #                         driver.quit()
    #                         broswer_created = False
    #
    #     amazondata.disconnect_database()
    # else:
    #     print("Connect Database In Failure", flush=True)
