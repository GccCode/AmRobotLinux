#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazondata import AmazonData
import xlrd
import random
from datetime import date
from datetime import datetime
from datetime import timedelta


xls_file_array = ['apparel',
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

# xls_file_array = [ 'health']

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

def fix_all_unaccessible_ip(ipfile):
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
                            ip = line.strip('\n')
                            print(line.strip('\n'))
                            condition = 'ip=\'' + ip + '\''
                            status = amazondata.update_data('ip_pool', 'status', '\'ok\'', condition)
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

def get_all_accessible_ip():
    amazondata = AmazonData()
    status = amazondata.create_database('ip_info')
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database('ip_info')
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
                    column = asin + ' INT NOT NULL'
                    status = amazondata.add_keyword_column(db_name, table, asin, column)
                    if status == False:
                        print("keyword add column in failure..", flush=True)
                    else:
                        condition = 'date=\'' + cur_date.strftime("%Y-%m-%d") + '\''
                        status = amazondata.update_data_autoinc(table, asin, condition)
                        if status == False:
                            print("keyword asin update data in failure..", flush=True)
    return status

def get_ramdon_accessible_ip(ips_array):
    if ips_array != False:
        return ips_array[random.randint(0, (len(ips_array) - 1))][0]
    else:
        return False


def mark_unaccessible_ip(ip):
    amazondata = AmazonData()
    status = amazondata.create_database('ip_info')
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database('ip_info')
        if status == False:
            print("connect in failure..", flush=True)
        else:
            condition = 'ip=\'' + ip + '\''
            status = amazondata.update_data('ip_pool', 'status', '\'no\'', condition)

    return status

def insert_all_node_info():
    amazondata = AmazonData()
    status = amazondata.create_database('node_info')
    if status == False:
        print("node_info create in failure..", flush=True)
    else:
        status = amazondata.connect_database('node_info')
        if status == False:
            print("connect in failure..", flush=True)
        else:
            for index in range(len(xls_file_array)):
                filename = '../xls/' + xls_file_array[index] + '.xls'
                workbook = xlrd.open_workbook(filename)
                # worksheets = workbook.sheet_names()
                # print('%s - worksheets is %s' % (index, worksheets))
                print(xls_file_array[index])
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

def get_all_node_name():
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
        else:
            print("get node name in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()

    return False

def get_all_data(db_name, table_name, column):
    table_array = []
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        if column == False:
            sql = 'select * from ' + table_name
        else:
            sql = 'select ' + column + ' from ' +table_name
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
        asin_array = get_all_data(db_name, (node + '_BS'), 'asin')
        if asin_array != False:
            for index in range(len(asin_array)):
                # print(asin_array[index])
                condition = 'asin=\'' + asin_array[index][0] + '\'' + ' and status=\'err\''
                amazondata.update_data(node + '_BS', 'status', '\'ok\'', condition)
        amazondata.disconnect_database()

def update_all_task_status():
    db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        node_array = get_all_data(db_name, 'SALE_TASK', 'node')
        for index in range(len(node_array)):
            update_asin_status_ok('amazondata', node_array[index][0])
        amazondata.disconnect_database()

def average_all_task():
    db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        node_array = get_all_data(db_name, 'SALE_TASK', 'node')
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

def update_all_task_date(db_name, date):
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        node_array = get_all_data(db_name, 'SALE_TASK', 'node')
        for index in range(len(node_array)):
            # print(asin_array[index])
            condition = 'node=\'' + node_array[index][0] + '\''
            amazondata.update_data('SALE_TASK', 'last_date', '\'' + date + '\'', condition)
            update_asin_status_ok('amazondata', node_array[index][0])
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
    update_click_data('amkiller', 'tree swing', 'B0746QS8T2')
