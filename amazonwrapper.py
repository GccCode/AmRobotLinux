#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazondata import AmazonData
import xlrd
import random
from datetime import date
from datetime import timedelta
import amazonglobal
import time
import traceback


xls_file_array_jp = ['apparel',
                  'automotive',
                  'baby',
                  'beauty',
                  'ce',
                  'computers',
                  'hobby',
                  'kitchen',
                  'office_products',
                  'pet_supplies',
                  'shoes',
                  'sports',
                  'tools',
                  'toys',
                  'health']

xls_file_array_us = ['automotive',
                  'baby',
                  'beauty',
                  'cell_phones',
                  'electronics',
                  'fashion',
                  'garden',
                  'home_improvement',
                  'pet_supplies',
                  'home_kitchen',
                  'office_products',
                  'sporting_goods',
                  'toys_games'
                  ]

def isDigit(x):
    try:
        x=int(x)
        return isinstance(x,int)
    except ValueError:
        return False


def insert_all_ip_info(ipfile):
    amazondata = AmazonData()
    status = amazondata.create_database('ip_info')
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database('ip_info')
        if status == False:
            print("connect in failure..", flush=True)
        else:
            status = amazondata.create_ip_table('ip_pool')
            if status != False:
                try:
                    f = open(ipfile)  # 返回一个文件对象
                    line = f.readline()  # 调用文件的 readline()方法
                    while line:
                        if '.' in line:
                            data = {
                                'ip': line.strip('\n'),
                                'status': 'ok'
                            }
                            print(line.strip('\n'))
                            status = amazondata.insert_ip_info_data('ip_pool', data)
                            if status == False:
                                break
                        line = f.readline()

                    f.close()
                except Exception as e:
                    print(str(e), flush=True)
                    status = False
                finally:
                    amazondata.disconnect_database()

    return status

def delete_sale_inventory_table(country, node):
    if country == 'us':
        db_name = amazonglobal.db_name_data_us
    elif country == 'jp':
        db_name = amazonglobal.db_name_data_jp
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        try:
            asin_info_array = get_all_data(db_name, node + '_BS', 'asin', False)
            for index in range(len(asin_info_array)):
                print(asin_info_array[index][0], flush=True)
                table = 'INVENTORY_' + asin_info_array[index][0]
                sql = 'drop table ' + table
                if amazondata.is_table_exsist(table):
                    status = amazondata.query(sql)
                    if status == False:
                        print("delete inventory table in failure..", flush=True)
                    else:
                        print('ok..', flush=True)
                table = 'SALE_' + asin_info_array[index][0]
                sql = 'drop table ' + table
                if amazondata.is_table_exsist(table):
                    status = amazondata.query(sql)
                    if status == False:
                        print("delete sale table in failure..", flush=True)
                    else:
                        print('ok..', flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
        finally:
            amazondata.disconnect_database()

def delete_sale_task(country, task_delete_file):
    db_name = amazonglobal.db_name_task
    if country == 'us':
        sale_task_table = amazonglobal.table_sale_task_us
    elif country == 'jp':
        sale_task_table = amazonglobal.table_sale_task_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("amazontask create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            try:
                f = open(task_delete_file)  # 返回一个文件对象
                line = f.readline()  # 调用文件的 readline()方法
                while line: # name:asin:keyword:type
                    tmp_line = line.strip('\n')
                    # delete_sale_inventory_table(country, tmp_line)
                    sql = 'delete from ' + sale_task_table + ' where node=\'' + tmp_line + '\''
                    # print(sql, flush=True)
                    # print(db_name, flush=True)
                    # print(sale_task_table, flush=True)
                    status = amazondata.query(sql)
                    if status == False:
                        print("delete node in sale_task_table in failure", flush=True)
                        break
                    else:
                        status = insert_task_delete_data(country, tmp_line)
                        if status == False:
                            print("insert task delete in failure", flush=True)
                            break
                    line = f.readline()
                    time.sleep(0.5)

                f.close()
            except Exception as e:
                print(str(e), flush=True)
                status = False
            finally:
                amazondata.disconnect_database()

    return status

def insert_task_delete_data(country, node):
    db_name = amazonglobal.db_name_task
    if country == 'us':
        task_delete_table = amazonglobal.table_sale_task_delete_us
    elif country == 'jp':
        task_delete_table = amazonglobal.table_sale_task_delete_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("database create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            status = amazondata.create_task_delete_table(task_delete_table)
            if status != False:
                try:
                    data = {
                        'node': node
                    }
                    status = amazondata.insert_rank_data(task_delete_table, data)
                    if status == False:
                        print("insert data in failure", flush=True)
                except Exception:
                    print(traceback.format_exc(), flush=True)
                    status = False
            amazondata.disconnect_database()

    return status

def is_in_task_delete_data(country, node):
    db_name = amazonglobal.db_name_task
    if country == 'us':
        task_delete_table = amazonglobal.table_sale_task_delete_us
    elif country == 'jp':
        task_delete_table = amazonglobal.table_sale_task_delete_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("database create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            status = amazondata.create_task_delete_table(task_delete_table)
            if status != False:
                try:
                    sql = 'select * from ' + task_delete_table + ' where node=\'' + node + '\''
                    cursor = amazondata.query(sql)
                    if cursor == False:
                        status = cursor
                    else:
                        status = True
                except Exception:
                    print(traceback.format_exc(), flush=True)
                    status = False
            amazondata.disconnect_database()

    return status

def insert_all_keyword(rank_file, country):
    db_name = amazonglobal.db_name_rank_task
    if country == 'us':
        rank_task_table = amazonglobal.table_rank_task_us
    elif country == 'jp':
        rank_task_table = amazonglobal.table_rank_task_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            status = amazondata.create_rank_task_table(rank_task_table)
            if status != False:
                try:
                    yesterday = date.today() + timedelta(days=-1)
                    f = open(rank_file)  # 返回一个文件对象
                    line = f.readline()  # 调用文件的 readline()方法
                    while line: # name:asin:keyword:type
                        if ':' in line:
                            tmp_line = line.strip('\n')
                            asin_info = tmp_line.split(':')
                            data = {
                                'name': asin_info[0],
                                'asin': asin_info[1],
                                'keyword': asin_info[2],
                                'type': asin_info[3],
                                'last_date': yesterday.strftime("%Y-%m-%d"),
                                'status': 'ok'
                            }
                            print(line.strip('\n'))
                            status = amazondata.insert_rank_data(rank_task_table, data)
                            if status == False:
                                break
                        line = f.readline()

                    f.close()
                except Exception as e:
                    print(str(e), flush=True)
                    status = False
                finally:
                    amazondata.disconnect_database()

    return status

def fix_all_unaccessible_ip(country, ipfile):
    if country == 'us':
        db_name = amazonglobal.db_name_ip_info_us
    elif country == 'jp':
        db_name = amazonglobal.db_name_ip_info_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            status = amazondata.create_ip_table(amazonglobal.table_ip_pool)
            if status != False:
                try:
                    f = open(ipfile)  # 返回一个文件对象
                    line = f.readline()  # 调用文件的 readline()方法
                    while line:
                        if '.' in line:
                            ip = line.strip('\n')
                            print(line.strip('\n'))
                            condition = 'ip=\'' + ip + '\''
                            status = amazondata.update_data(amazonglobal.table_ip_pool, 'status', '\'ok\'', condition)
                            if status == False:
                                break
                        line = f.readline()

                    f.close()
                except Exception as e:
                    print(str(e), flush=True)
                    status = False
                finally:
                    amazondata.disconnect_database()

    return status

def get_all_accessible_ip(country):
    if country == 'us':
        db_name = amazonglobal.db_name_ip_info_us
    elif country == 'jp':
        db_name = amazonglobal.db_name_ip_info_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            sql = 'select ip from ip_pool where status=\'ok\''
            cursor = amazondata.query(sql)
            if cursor != False:
                if cursor.rowcount > 0:
                    ips_array = cursor.fetchall()
                    status = ips_array
                else:
                    status = False
            else:
                status = False
            amazondata.disconnect_database()

    return status

def update_click_data(db_name, keyword, asin):
    table = keyword.replace(' ', '_')
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("amkiller database created in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("amkiller database connected in failure..", flush=True)
        else:
            status = amazondata.create_amkiller_keyword_table(table)
            if status == False:
                print("keyword table created in failure..", flush=True)
            else:
                cur_date = date.today()
                data = {
                    'date': cur_date
                }
                status = amazondata.insert_amkiller_keyword_data(table, data)
                if status == False:
                    print("keyword insert data in failure..", flush=True)
                else:
                    column = asin + ' INT default 0'
                    status = amazondata.add_keyword_column(db_name, table, asin, column)
                    if status == False:
                        print("keyword add column in failure..", flush=True)
                    else:
                        condition = 'date=\'' + cur_date.strftime("%Y-%m-%d") + '\''
                        status = amazondata.update_data_autoinc(table, asin, condition)
                        if status == False:
                            print("keyword asin update data in failure..", flush=True)
                amazondata.disconnect_database()
    return status

def update_rank_data(db_name, table, keyword, type, rank_info):
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("database created in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("database connected in failure..", flush=True)
        else:
            status = amazondata.create_rank_keyword_table(table)
            if status == False:
                print("rank keyword table created in failure..", flush=True)
            else:
                cur_date = date.today()
                data = {
                    'keyword': keyword,
                    'type': type
                }
                status = amazondata.insert_rank_data(table, data)
                if status == False:
                    print("keyword insert in failure..", flush=True)
                else:
                    rank = int(rank_info[0]) * 100 + int(rank_info[1])
                    column = cur_date.strftime("%Y_%m_%d") + ' int not null default 9999'
                    status = amazondata.add_rank_column(db_name, table, cur_date.strftime("%Y_%m_%d"), column)
                    if status == False:
                        print("keyword add column in failure..", flush=True)
                    else:
                        condition = 'keyword=\'' + keyword + '\' and type=\'' + type + '\''
                        status = amazondata.update_data(table, cur_date.strftime("%Y_%m_%d"),  rank, condition)
                        if status == False:
                            print("keyword rank update data in failure..", flush=True)
                        else:
                            pass
            amazondata.disconnect_database()

    return status

def update_rank_task_run_status(country, keyword, entry_type, run_status):
    db_name = amazonglobal.db_name_rank_task
    if country == 'us':
        table = amazonglobal.table_rank_task_us
    elif country == 'jp':
        table = amazonglobal.table_rank_task_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            condition = 'keyword=\'' + keyword + '\' and type=\'' + entry_type + '\''
            status = amazondata.update_data(table, 'status', '\'' + run_status + '\'', condition)
            if status == False:
                print("update rank task run_status in failure ", flush=True)
        amazondata.disconnect_database()

    return status

def update_rank_task_date(country, keyword, entry_type):
    db_name = amazonglobal.db_name_rank_task
    if country == 'us':
        table = amazonglobal.table_rank_task_us
    elif country == 'jp':
        table = amazonglobal.table_rank_task_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            condition = 'keyword=\'' + keyword + '\' and type=\'' + entry_type + '\''
            cur_date = date.today()
            value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
            status = amazondata.update_data(table, 'last_date', value, condition)
            if status == False:
                print("update rank task last_date in failure ", flush=True)
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
        sql = 'select status from ' + table + ' where node=\'' + node + '\' and last_date <> ' + value + ' limit 1'
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
            sql = 'select status from ' + node_table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>10' + ' and inventory_date <> ' + value + ' limit 1'
        elif country == 'jp':
            sql = 'select status from ' + node_table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>800' + ' and inventory_date <> ' + value + ' limit 1'
        status = amazondata.select_data(sql)
        if status == False:
            status = True
        else:
            status = False

        amazondata.disconnect_database()

    return status

def get_ramdon_accessible_ip(ips_array):
    if ips_array != False:
        return ips_array[random.randint(0, (len(ips_array) - 1))][0]
    else:
        return False


def mark_unaccessible_ip(country, ip):
    if country == 'us':
        db_name = amazonglobal.db_name_ip_info_us
    elif country == 'jp':
        db_name = amazonglobal.db_name_ip_info_jp
    amazondata = AmazonData()
    status = amazondata.create_database(db_name)
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            condition = 'ip=\'' + ip + '\''
            status = amazondata.update_data('ip_pool', 'status', '\'no\'', condition)
            amazondata.disconnect_database()

    return status

def insert_all_node_info(xls_file_array):
    amazondata = AmazonData()
    status = amazondata.create_database('node_info_us')
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database('node_info_us')
        if status == False:
            print("connect in failure..", flush=True)
        else:
            for index in range(len(xls_file_array)):
                filename = '../xls/' + xls_file_array[index] + '.xls'
                workbook = xlrd.open_workbook(filename)
                # worksheets = workbook.sheet_names()
                # print('%s - worksheets is %s' % (index, worksheets))
                print(xls_file_array[index], flush=True)
                status = amazondata.create_node_info_table(xls_file_array[index])
                if status == False:
                    print("create note info table in failure..", flush=True)
                else:
                    worksheet1 = workbook.sheet_by_index(1)
                    # print(worksheet1.name)
                    num_rows = worksheet1.nrows
                    for curr_row in range(1, num_rows):
                        row = worksheet1.row_values(curr_row)
                        # print(str(row[0]).split('.')[0])
                        data = {
                            'node': str(row[0]).split('.')[0],
                            'name': row[1]
                        }
                        status = amazondata.insert_node_info_data(xls_file_array[index], data)
                        if status == False:
                            print("insert %s in failure..", flush=True)
                        # print('row%s is %s' % (curr_row, row))

        amazondata.disconnect_database()

def delete_column(db_name, condition, column_name):
    table_array = get_all_table(db_name, condition)
    if table_array != False:
        amazondata = AmazonData()
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            for table in table_array:
                status = amazondata.delete_column(db_name, table, column_name)
                if status == False:
                    print("delete column in failure..", flush=True)
                    return False

            amazondata.disconnect_database()

    return False

def get_one_data(db_name, table, condition):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        if condition != False:
            sql = 'select * from ' + table + ' where ' + condition
        else:
            sql = 'select * from ' + table
        cursor = amazondata.query(sql)
        if cursor != False:
            result = cursor.fetchone()
            print(result, flush=True)
            return result
        else:
            print("get one data in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()

    return False

def update_data(db_name, table, key, value, condition):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        status = amazondata.update_data(table, key, value, condition)
        if status == False:
            print("update data in failure.. + " + db_name, flush=True)
        amazondata.disconnect_database()

    return status

def add_new_column(db_name, condition, column_name, column):
    table_array = get_all_table(db_name, condition)
    if table_array != False:
        amazondata = AmazonData()
        status = amazondata.connect_database(db_name)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            for table in table_array:
                status = amazondata.add_column(db_name, table, column_name, column)
                if status == False:
                    print("add column in failure..", flush=True)
                    return False

            amazondata.disconnect_database()

    return False

def delete_tables(db_name, condition):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        sql = 'SHOW TABLES'
        cursor = amazondata.query(sql)
        if cursor != False:
            result = cursor.fetchall()
            for index in range(len(result)):
                if condition in result[index][0]:
                    delete_sql = 'drop table ' + result[index][0]
                    print(delete_sql, flush=True)
                    cursor = amazondata.query(delete_sql)
                    # if cursor == False:
                    #     print("delete table in failure.. + " + db_name, flush=True)
        else:
            print("get all table in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()

    return False

def get_all_table(db_name, condition):
    table_array= []
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        sql = 'SHOW TABLES'
        cursor = amazondata.query(sql)
        if cursor != False:
            result = cursor.fetchall()
            if condition == False:
                for index in range(len(result)):
                    table_array.append(result[index][0])
            else:
                for index in range(len(result)):
                    if condition in result[index][0]:
                        # print(result[index][0])
                        table_array.append(result[index][0])
        else:
            print("get all table in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()
        if len(table_array) != 0:
            print(table_array)
            return table_array

    return False

def get_all_node_name(xls_file_array):
    amazondata = AmazonData()
    status = amazondata.connect_database('amazontask')
    if status == False:
        print("connect in failure..", flush=True)
    else:
        node_array = get_all_data('amazontask', 'SALE_TASK', 'node')
        if node_array != False:
            for index in range(len(node_array)):
                print(node_array[index][0], flush=True)
                for node_table in xls_file_array:
                    print(node_table, flush=True)
                    node_name = get_node_name('node_info', node_table, node_array[index][0])
                    if node_name != False:
                        print(node_name[0][1], flush=True)
                        condition = 'node=\'' + node_array[index][0] + '\''
                        status = amazondata.update_data('SALE_TASK', 'node_name', '\'' + node_name[0][1] + '\'', condition)
                        if status == False:
                            return False
                        break
                        # return node_name[1]
        amazondata.disconnect_database()

    return False

def get_node_name(db_name, table_name, node):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        sql = 'select * from ' + table_name + ' where node=\'' + node + '\''
        cursor = amazondata.query(sql)
        if cursor != False:
            if cursor.rowcount > 0:
                result = cursor.fetchall()
                # print(result)
                return result

        amazondata.disconnect_database()

    return False

def get_node_name_from_all(db_name, node, country):
    if country == 'us':
        node_table_array = xls_file_array_us
    elif country == 'jp':
        node_table_array = xls_file_array_jp

    for node_table in node_table_array:
        result = get_node_name(db_name, node_table, node)
        if result != False:
            return result[0][1]

    return False

def get_all_data(db_name, table_name, column, condition):
    table_array = []
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        if column == False:
            if condition == False:
                sql = 'select * from ' + table_name
            else:
                sql = 'select * from ' + table_name + ' where ' + condition
        else:
            if condition == False:
                sql = 'select ' + column + ' from ' +table_name
            else:
                sql = 'select ' + column + ' from ' + table_name + ' where ' + condition
        cursor = amazondata.query(sql)
        if cursor != False:
            if cursor.rowcount > 0:
                result = cursor.fetchall()
                # print(result)
                return result
        else:
            print("get all table in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()

    return False

def update_asin_status_ok(db_name, node):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        asin_array = get_all_data(db_name, (node + '_BS'), 'asin', False)
        if asin_array != False:
            for index in range(len(asin_array)):
                # print(asin_array[index])
                condition = 'asin=\'' + asin_array[index][0] + '\'' + ' and status=\'err\''
                amazondata.update_data(node + '_BS', 'status', '\'ok\'', condition)
        amazondata.disconnect_database()

def update_all_task_status(db_name, table, country):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        condition = False # 'length(node)>4'
        node_array = get_all_data(db_name, table, 'node', condition)
        for index in range(len(node_array)):
            if country == 'jp':
                update_asin_status_ok('data_jp', node_array[index][0])
            elif country == 'us':
                update_asin_status_ok('data_us', node_array[index][0])
        amazondata.disconnect_database()

def average_all_task():
    db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        node_array = get_all_data(db_name, 'SALE_TASK', 'node', False)
        limit = int(len(node_array) / 3)
        for index in range(len(node_array)):
            # print(asin_array[index])
            condition = 'node=\'' + node_array[index][0] + '\''
            if index < limit:
                amazondata.update_data('SALE_TASK', 'task_id', '\'1\'', condition)
            elif index >= limit and index <= (limit * 2):
                amazondata.update_data('SALE_TASK', 'task_id', '\'2\'', condition)
            else:
                amazondata.update_data('SALE_TASK', 'task_id', '\'3\'', condition)
        amazondata.disconnect_database()

def update_all_task_date_status(db_name, date, country):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        if country == 'jp':
            task_table = amazonglobal.table_sale_task_jp
            data_db = amazonglobal.db_name_data_jp
        elif country == 'us':
            task_table = amazonglobal.table_sale_task_us
            data_db = amazonglobal.db_name_data_us

        node_array = get_all_data(db_name, task_table, 'node', False)
        for index in range(len(node_array)):
            # print(asin_array[index])
            condition = 'node=\'' + node_array[index][0] + '\''
            amazondata.update_data(task_table, 'last_date', '\'' + date + '\'', condition)
            amazondata.update_data(task_table, 'status', '\'' + 'ok' + '\'', condition)
            update_asin_status_ok(data_db, node_array[index][0])
        amazondata.disconnect_database()

def update_all_rank_task_date_status(date, country):
    if country == 'jp':
        task_table = amazonglobal.table_rank_task_jp
        db_name = amazonglobal.db_name_rank_task
    elif country == 'us':
        task_table = amazonglobal.table_rank_task_us
        db_name = amazonglobal.db_name_rank_task
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        id_array = get_all_data(db_name, task_table, 'id', False)
        for index in range(len(id_array)):
            # print(asin_array[index])
            condition = 'id=' + str(id_array[index][0])
            amazondata.update_data(task_table, 'last_date', '\'' + date + '\'', condition)
            amazondata.update_data(task_table, 'status', '\'' + 'ok' + '\'', condition)
        amazondata.disconnect_database()


# SELECT CREATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='amazondata' AND TABLE_NAME='INVENTORY_B07GYTTF8B';
if __name__ == "__main__":
    # amazondata = AmazonData()
    # status = amazondata.connect_database('amazondata')
    # if status == False:
    #     print("connect in failure..", flush=True)
    # else:
    #     pass
    # get_all_table('amazondata', '_BS')
    # get_all_data('amazondata', '2201158051_BS', False)
    # update_asin_status_ok('amazondata', '2189296051')
    # update_all_task_date('amazontask', '2018-10-06')
    # insert_all_node_info()
    # insert_all_ip_info('../myproxy.txt')
    # update_all_task_status()
    # print(get_ramdon_accessible_ip()) 196.16.109.149:8000
    # mark_unaccessible_ip('196.16.109.149:8000')
    # fix_all_unaccessible_ip('../fix_ip.txt')
    # average_all_task()
    # get_all_node_name()
    # update_click_data('amkiller', 'tree swing', 'B0746QS8T2')
    # insert_all_node_info(xls_file_array_us)
    # delete_column('node_info', 'ce', 'status')
    # add_new_column('node_info', 'ce', 'status', 'status VARCHAR(5) default \'no\' check(status in(\'no\', \'run\', \'yes\', \'err\'))')
    # delete_column('node_info_us', 'automotive', 'status')
    # update_all_task_status('amazontask', 'sale_task_us', 'us')
    # get_one_data('node_info_us', 'automotive', False)
    delete_sale_task('us', 'task_delete.txt')
