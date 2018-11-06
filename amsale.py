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
from sqlmgr import SqlMgr


def update_task_node(amazondata, table, node):
    cur_date = date.today()
    condition = 'node=\'' + node + '\''
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    status = amazondata.update_data(table, 'last_date', value, condition)

    return status


def update_asin_status_err(am, node, asin):
    condition = 'asin=\'' + asin + '\''
    return am.update_data(node + '_BS', 'status', '\'err\'', condition)


def is_token_runout(amazondata):
    table = amazonglobal.table_token
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

    return status


def is_task_running(amazondata):
    table = amazonglobal.table_sale_task_status
    status = amazondata.create_task_status_table(table)
    if status == False:
        print("create task status table in failure...", flush=True)
    else:
        sql = 'select status from ' + table + ' where status=\'stop\' limit 1'
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

    return status


def update_token_count(amazondata):
    table = amazonglobal.table_token
    condition = 'count=0'
    status = amazondata.update_data(table, 'count', 100, condition)

    return status


def desc_token_count(amazondata):
    table = amazonglobal.table_token
    condition = 'count<>0'
    status = amazondata.update_data_autodes(table, 'count', condition)

    return status


def get_asin_rows_from_node(amazondata, table):
    status = False
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    if amazondata.country == 'us':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>=12 and inventory_date <> ' + value
    elif amazondata.country == 'jp':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>800' + ' and inventory_date <> ' + value
    cursor = amazondata.select_data(sql)
    if cursor == False:
        print("Get Asin_Rows From Node In Failure" + table, flush=True)
        status = False
    else:
        status = cursor

    return status

def get_seller_name(ad, country, table):
    status = False
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    if country == 'us':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>=19 and inventory_date <> ' + value
    elif country == 'jp':
        sql = 'select * from ' + table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>800' + ' and inventory_date <> ' + value
    cursor = ad.select_data(sql)
    if cursor == False:
        print("Get Asin_Rows From Node In Failure" + table, flush=True)
        status = False
    else:
        status = cursor

    return status

def amsale_from_mysql(sqlmgr, node_type):
    ips_array = amazonwrapper.get_all_accessible_ip(sqlmgr.ad_ip_info)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)

    amazonspider = AmazonSpider()

    status = False
    if sqlmgr.country == 'us':
        task_table = amazonglobal.table_sale_task_us
    elif sqlmgr.country == 'jp':
        task_table = amazonglobal.table_sale_task_jp

    try:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        status_condition = 'status<>\'no\' and last_date<>' + value
        node_task = amazonwrapper.get_one_data(sqlmgr.ad_sale_task, task_table, status_condition)
        while node_task != False:
            t1 = time.time()
            node = node_task[0]
            node_table = node + '_' + node_type
            sql_condition = 'node=' + '\'' + node + '\''
            status = amazonwrapper.update_data(sqlmgr.ad_sale_task, task_table, 'status', '\'no\'', sql_condition)
            if status != False:
                while amazonwrapper.is_task_finish(sqlmgr.ad_sale_task, task_table, node) == False:
                    total_count = 0
                    while amazonwrapper.is_all_inventory_finish(sqlmgr.ad_sale_data, node_table) == False:
                        asin_cursor = get_asin_rows_from_node(sqlmgr.ad_sale_data, node_table)
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
                                    if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")) and asin_info[8] > 0  and asin_info[8] < 4 and asin_info[7] != 'FBM' and float(asin_info[3]) > 12:
                                        status = True
                                elif country == 'jp':
                                    if asin_info[11] == 'no' and asin_info[13] == 'ok' and str(asin_info[10]) != str(date.today().strftime("%Y-%m-%d")) and asin_info[8] > 0  and asin_info[8] < 4 and asin_info[7] != 'FBM' and float(asin_info[3]) > 800:
                                        status = True
                                if status == True:
                                    if country == 'jp':
                                        result = amazonspider.get_inventory_jp(sqlmgr, False, asin, ips_array, True)
                                    elif country == 'us':
                                        if asin_info[14] == '':
                                            result = amazonspider.get_inventory_us(sqlmgr, False, asin, ips_array, False, True)
                                        else:
                                            result = amazonspider.get_inventory_us(sqlmgr, False, asin, ips_array, asin_info[14], True)
                                    if result != False and result != -111 and result != -222:
                                        cur_date = date.today()
                                        data = {
                                            'date': cur_date,
                                            'inventory': result['inventory']
                                        }
                                        condition = 'asin=\'' + asin + '\''
                                        if asin_info[14] == '':
                                            status = sqlmgr.ad_sale_data.update_data(node_table, 'seller_name', '\'' + result['seller_name'] + '\'', condition)
                                            if status == False:
                                                print("update seller_name in failure", flush=True)
                                                return status
                                        if asin_info[15] == '':
                                            status = sqlmgr.ad_sale_data.update_data(node_table, 'size', '\'' + result['size'] + '\'', condition)
                                            if status == False:
                                                print("update size in failure", flush=True)
                                                return status
                                        if asin_info[16] == 0:
                                            status = sqlmgr.ad_sale_data.update_data(node_table, 'weight', result['weight'], condition)
                                            if status == False:
                                                print("update weight in failure", flush=True)
                                                return status
                                        if result['limited'] == 'yes':
                                            status = sqlmgr.ad_sale_data.update_data(node_table, 'limited', '\'yes\'', condition)
                                        else:
                                            inventory_table = 'INVENTORY_' + asin
                                            if sqlmgr.ad_sale_data.is_table_exsist(inventory_table) == False:
                                                status = sqlmgr.ad_sale_data.create_inventory_table(inventory_table)
                                                if status == False:
                                                    print("create invetory table in failure...", flush=True)
                                            yesterday_inventory = sqlmgr.ad_sale_data.get_yesterday_inventory(inventory_table)
                                            if (yesterday_inventory / data['inventory']) > 10:
                                                print("get inventory may error.. yesterday " + str(yesterday_inventory) + ' today ' + str(data['inventory']), flush=True)
                                                status = update_asin_status_err(sqlmgr.ad_sale_data, node, asin)
                                                if status == False:
                                                    print("update asin status faild.. + " + node + ' ' + asin, flush=True)
                                            else:
                                                status = sqlmgr.ad_sale_data.insert_inventory_data(inventory_table, data)
                                                if status == True:
                                                    total_count += 1
                                                    condition = 'asin=\'' + asin + '\''
                                                    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                                    status = sqlmgr.ad_sale_data.update_data(node_table, 'inventory_date', value, condition)
                                                    if status == True:
                                                        status = sqlmgr.ad_sale_data.get_yesterday_sale(inventory_table)
                                                        if status != -999:
                                                            yesterday = date.today() + timedelta(days=-1)
                                                            data = {
                                                                'date': yesterday,
                                                                'sale': copy.deepcopy(status)
                                                            }
                                                            sale_table = 'SALE_' + asin
                                                            status = sqlmgr.ad_sale_data.create_sale_table(sale_table)
                                                            if status == True:
                                                                status = sqlmgr.ad_sale_data.insert_sale_data(sale_table, data)
                                                                if status == True:
                                                                    avg_sale = sqlmgr.ad_sale_data.get_column_avg(sale_table, 'sale')
                                                                    if avg_sale != -999:
                                                                        status = sqlmgr.ad_sale_data.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                                        if status == False:
                                                                            print("avg_sale update fail.. + " + node_table, flush=True)
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
                                            ips_array = amazonwrapper.get_all_accessible_ip(sqlmgr.ad_ip_info)
                                            if ips_array == False:
                                                print("no accessible ip", flush=True)
                                                exit(-1)
                                            status = False
                                            continue
                                        elif result == -222:
                                            # print("overweight " + asin, flush=True)
                                            condition = 'asin=\'' + asin + '\''
                                            status = sqlmgr.ad_sale_data.update_data(node_table, 'limited', '\'yes\'', condition)
                                            if status == False:
                                                print("update data for limited in failure", flush=True)
                                        else:
                                            print("Get Inventory In Failure " + asin, flush=True)
                                        status = update_asin_status_err(sqlmgr.ad_sale_data, node, asin)
                                        if status == False:
                                            print("update asin status faild.. + " + node + ' ' + asin, flush=True)

                    if amazonwrapper.is_all_inventory_finish(sqlmgr.ad_sale_data, node_table) == True:
                        status = update_task_node(sqlmgr.ad_sale_task, task_table, node)
                        if status == False:
                            print("update task node failed.. + " + node, flush=True)

                        status = amazonwrapper.update_data(sqlmgr.ad_sale_task, task_table, 'status', '\'ok\'', sql_condition)
                        if status == False:
                            print("update status in failure " + node, flush=True)

                    t2 = time.time()
                    print("Asin_Count-Time_Consumed：" + str(total_count) + '-' + format(t2 - t1), flush=True)
            node_task = amazonwrapper.get_one_data(sqlmgr.ad_sale_task, task_table, status_condition)
    except Exception:
        print(traceback.format_exc(), flush=True)
        amazonwrapper.update_data(sqlmgr.ad_sale_task, task_table, 'status', '\'ok\'', sql_condition)
        exit()


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    task = sys.argv[1]
    country = sys.argv[2]

    sqlmgr = SqlMgr(country)
    if sqlmgr.start() == False:
        print("SqlMgr initialized in failure", flush=True)
        exit()

    if task == 'run':
        type = sys.argv[3]
        while is_task_running(sqlmgr.ad_sale_task):
            while is_token_runout(sqlmgr.ad_token) == False:
                status = desc_token_count(sqlmgr.ad_token)
                if status == False:
                    print('desc token count in failure...', flush=True)
                    exit(-1)
                amsale_from_mysql(sqlmgr, type)

        time.sleep(300)
        print("task is not running...", flush=True)

    elif task == 'fix':
        only_token = sys.argv[3]
        today = date.today()
        yesterday = date.today() + timedelta(days=-1)
        if only_token == '0':
            amazonwrapper.update_all_task_date_status(sqlmgr, yesterday.strftime("%Y-%m-%d"))
        if is_token_runout(sqlmgr.ad_token):
            status = update_token_count(sqlmgr.ad_token)
            if status == False:
                print('update token count in failure...', flush=True)
            else:
                print("update token count ok...", flush=True)
        else:
            print('token not runout now...', flush=True)

        time.sleep(60)

    sqlmgr.stop()
