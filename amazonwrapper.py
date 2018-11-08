#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazondata import AmazonData
import xlrd
import random
from time import strftime, localtime
import calendar
import datetime as dt
from datetime import date
from datetime import timedelta
import amazonglobal
import time
import traceback
from sqlmgr import SqlMgr


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
                  'toys_games',
                  'health']


'''获取当前日期前后N天或N月的日期'''

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())


def today():
    return date.today()


def todaystr():
    '''
    get date string, date format="YYYYMMDD"
    '''
    return year + mon + day


def datetime():
    '''''
    get datetime,format="YYYY-MM-DD HH:MM:SS"
    '''
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def datetimestr():
    '''''
    get datetime string
    date format="YYYYMMDDHHMMSS"
    '''
    return year + mon + day + hour + min + sec


def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)

def get_days_array_of_day(n, direction):
    days_array = []
    if direction >=0:
        for i in range(0, (n+1)):
            index = i * direction
            str_date = get_day_of_day(index).strftime('%Y-%m-%d')
            days_array.append(str_date)
    else:
        for i in range(n+1):
            index = n * direction + i
            str_date = get_day_of_day(index).strftime('%Y-%m-%d')
            days_array.append(str_date)

    return days_array


def get_days_of_month(year, mon):
    '''''
    get days of month
    '''
    return calendar.monthrange(year, mon)[1]


def get_firstday_of_month(year, mon):
    '''''
    get the first day of month
    date format = "YYYY-MM-DD"
    '''
    days = "01"
    if (int(mon) < 10):
        mon = "0" + str(int(mon))
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_lastday_of_month(year, mon):
    '''''
    get the last day of month
    date format = "YYYY-MM-DD"
    '''
    days = calendar.monthrange(year, mon)[1]
    mon = addzero(mon)
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_firstday_month(n=0):
    '''''
    get the first day of month from today
    n is how many months
    '''
    (y, m, d) = getyearandmonth(n)
    d = "01"
    arr = (y, m, d)
    return "-".join("%s" % i for i in arr)


def get_lastday_month(n=0):
    '''''
    get the last day of month from today
    n is how many months
    '''
    return "-".join("%s" % i for i in getyearandmonth(n))


def getyearandmonth(n=0):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon + n
    if (n >= 0):
        if (totalmon <= 12):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)
    else:
        if ((totalmon > 0) and (totalmon < 12)):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)


def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if (nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs


def get_today_month(n=0):
    '''''
    获取当前日期前后N月的日期
    if n>0, 获取当前日期前N月的日期
    if n<0, 获取当前日期后N月的日期
    date format = "YYYY-MM-DD"
    '''
    (y, m, d) = getyearandmonth(n)
    arr = (y, m, d)
    if (int(day) < int(d)):
        arr = (y, m, day)
    return "-".join("%s" % i for i in arr)

def isDigit(x):
    try:
        x=int(x)
        return isinstance(x,int)
    except ValueError:
        return False

def insert_all_ip_info(sqlmgr, ipfile):
    status = sqlmgr.ad_ip_info.create_ip_table('ip_pool')
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
                    status = sqlmgr.ad_ip_info.insert_ip_info_data('ip_pool', data)
                    if status == False:
                        break
                line = f.readline()

            f.close()
        except Exception as e:
            print(str(e), flush=True)
            status = False

    return status

def delete_sale_inventory_table(sqlmgr, node):
    try:
        asin_info_array = get_all_data(sqlmgr.ad_sale_data, node + '_BS', 'asin', False)
        for index in range(len(asin_info_array)):
            print(asin_info_array[index][0], flush=True)
            table = 'INVENTORY_' + asin_info_array[index][0]
            sql = 'drop table ' + table
            if sqlmgr.ad_sale_data.is_table_exsist(table):
                status = sqlmgr.ad_sale_data.query(sql)
                if status == False:
                    print("delete inventory table in failure..", flush=True)

            table = 'SALE_' + asin_info_array[index][0]
            sql = 'drop table ' + table
            if sqlmgr.ad_sale_data.is_table_exsist(table):
                status = sqlmgr.ad_sale_data.query(sql)
                if status == False:
                    print("delete sale table in failure..", flush=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)


def delete_sale_task(sqlmgr, task_delete_file):
    if sqlmgr.country == 'us':
        sale_task_table = amazonglobal.table_sale_task_us
    elif sqlmgr.country == 'jp':
        sale_task_table = amazonglobal.table_sale_task_jp

    try:
        f = open(task_delete_file)  # 返回一个文件对象
        line = f.readline()  # 调用文件的 readline()方法
        while line: # name:asin:keyword:type
            tmp_line = line.strip('\n')
            sql = 'delete from ' + sale_task_table + ' where node=\'' + tmp_line + '\''
            status = sqlmgr.ad_sale_task.query(sql)
            if status == False:
                print("delete node in sale_task_table in failure", flush=True)
                break
            else:
                status = insert_task_delete_data(sqlmgr.ad_sale_task, tmp_line)
                if status == False:
                    print("insert task delete in failure", flush=True)
                    break
            line = f.readline()
            time.sleep(0.5)

        f.close()
    except Exception:
        print(traceback.format_exc(), flush=True)
        status = False

    return status

def insert_task_delete_data(amazondata, node):
    if amazondata.country == 'us':
        task_delete_table = amazonglobal.table_sale_task_delete_us
    elif amazondata.country == 'jp':
        task_delete_table = amazonglobal.table_sale_task_delete_jp

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

    return status

def is_in_task_delete_data(amazondata, node):
    if amazondata.country == 'us':
        task_delete_table = amazonglobal.table_sale_task_delete_us
    elif amazondata.country == 'jp':
        task_delete_table = amazonglobal.table_sale_task_delete_jp

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

    return status

def insert_all_keyword_into_task(rank_file, sqlmgr):
    if sqlmgr.country == 'us':
        rank_task_table = amazonglobal.table_rank_task_us
    elif sqlmgr.country == 'jp':
        rank_task_table = amazonglobal.table_rank_task_jp

    status = sqlmgr.ad_rank_task.create_rank_task_table(rank_task_table)
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
                    status = sqlmgr.ad_rank_task.insert_rank_data(rank_task_table, data)
                    if status == False:
                        break
                line = f.readline()

            f.close()
        except Exception:
            print(traceback.format_exc(), flush=True)
            status = False

    return status

def get_all_accessible_ip(amazondata):
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

def update_click_data(amazondata, keyword, asin):
    table = keyword.replace(' ', '_')
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
            status = amazondata.add_keyword_column(amazondata.db_name, table, asin, column)
            if status == False:
                print("keyword add column in failure..", flush=True)
            else:
                condition = 'date=\'' + cur_date.strftime("%Y-%m-%d") + '\''
                status = amazondata.update_data_autoinc(table, asin, condition)
                if status == False:
                    print("keyword asin update data in failure..", flush=True)

    return status

def update_rank_data(amazondata, table, keyword, type, rank_info):
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
            status = amazondata.add_rank_column(amazondata.db_name, table, cur_date.strftime("%Y_%m_%d"), column)
            if status == False:
                print("keyword add column in failure..", flush=True)
            else:
                condition = 'keyword=\'' + keyword + '\' and type=\'' + type + '\''
                status = amazondata.update_data(table, cur_date.strftime("%Y_%m_%d"),  rank, condition)
                if status == False:
                    print("keyword rank update data in failure..", flush=True)
                else:
                    pass

    return status

def update_rank_task_run_status(amazondata, keyword, entry_type, run_status):
    if amazondata.country == 'us':
        table = amazonglobal.table_rank_task_us
    elif amazondata.country == 'jp':
        table = amazonglobal.table_rank_task_jp

    condition = 'keyword=\'' + keyword + '\' and type=\'' + entry_type + '\''
    status = amazondata.update_data(table, 'status', '\'' + run_status + '\'', condition)
    if status == False:
        print("update rank task run_status in failure ", flush=True)

    return status

def update_rank_task_date(amazondata, keyword, entry_type):
    if amazondata.country == 'us':
        table = amazonglobal.table_rank_task_us
    elif amazondata.country == 'jp':
        table = amazonglobal.table_rank_task_jp

    condition = 'keyword=\'' + keyword + '\' and type=\'' + entry_type + '\''
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    status = amazondata.update_data(table, 'last_date', value, condition)
    if status == False:
        print("update rank task last_date in failure ", flush=True)

    return status

def is_task_finish(amazondata, table, node):
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    sql = 'select status from ' + table + ' where node=\'' + node + '\' and last_date <> ' + value + ' limit 1'
    status = amazondata.select_data(sql)
    if status == False:
        status = True
    else:
        status = False

    return status

def is_all_inventory_finish(amazondata, node_table):
    cur_date = date.today()
    value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
    if amazondata.country == 'us':
        sql = 'select status from ' + node_table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>=12' + ' and inventory_date <> ' + value + ' limit 1'
    elif amazondata.country == 'jp':
        sql = 'select status from ' + node_table + ' where limited=\'no\' and status=\'ok\' and seller>0 and seller<4 and shipping<>\'FBM\' and price>800' + ' and inventory_date <> ' + value + ' limit 1'
    status = amazondata.select_data(sql)
    if status == False:
        status = True
    else:
        status = False

    return status

def get_ramdon_accessible_ip(ips_array):
    if ips_array != False:
        return ips_array[random.randint(0, (len(ips_array) - 1))][0]
    else:
        return False


def mark_unaccessible_ip(amazondata, ip):
    condition = 'ip=\'' + ip + '\''
    status = amazondata.update_data('ip_pool', 'status', '\'no\'', condition)

    return status

def insert_all_node_info(amazondata, xls_file_array):
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


def delete_column(amazondata, condition, column_name):
    table_array = get_all_table(amazondata, condition)
    if table_array != False:
        for table in table_array:
            status = amazondata.delete_column(amazondata.db_name, table, column_name)
            if status == False:
                print("delete column in failure..", flush=True)
                return False

    return False


def get_one_data(amazondata, table, condition):
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
        print("get one data in failure.. + " + amazondata.db_name, flush=True)

    return False


def update_data(amazondata, table, key, value, condition):
    status = amazondata.update_data(table, key, value, condition)
    if status == False:
        print("update data in failure.. + " + amazondata.db_name, flush=True)

    return status


def add_new_column(amazondata, condition, column_name, column):
    table_array = get_all_table(amazondata, condition)
    if table_array is not False:
        count = 0
        for table in table_array:
            status = amazondata.add_column(amazondata.db_name, table, column_name, column)
            if status == False:
                print("add column in failure..", flush=True)
                return False
            else:
                print(count, flush=True)
                count += 1

    return False


def delete_tables(amazondata, table_name_condition, condition):
    if condition == False:
        sql = 'SHOW TABLES'
    else:
        sql = 'SHOW TABLES LIKE ' + condition
    cursor = amazondata.query(sql)
    if cursor != False:
        result = cursor.fetchall()
        for index in range(len(result)):
            if table_name_condition in result[index][0]:
                delete_sql = 'drop table ' + result[index][0]
                print(delete_sql, flush=True)
                cursor = amazondata.query(delete_sql)
                # if cursor == False:
                #     print("delete table in failure.. + " + db_name, flush=True)
    else:
        print("get all table in failure.. + " + amazondata.db_name, flush=True)

    return False


def get_table_existed_time(amazondata, table_name):
    now_time = dt.datetime.now()
    sql = 'select create_time from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = ' + '\'' + amazondata.db_name + '\'' + 'and TABLE_NAME =' + '\'' + table_name + '\''
    cursor = amazondata.query(sql)
    if cursor is not False:
        create_time_str = cursor.fetchone()[0].strftime('%Y-%m-%d %H:%M:%S')
        create_time = dt.datetime.strptime(create_time_str, '%Y-%m-%d %H:%M:%S')
        existed_time = now_time - create_time
        return int(existed_time.days)
    else:
        print("Err: get create time for table " + table_name, flush=True)
        return False

def is_table_expired(amazondata, table_name, valid_days):
    existed_days = get_table_existed_time(amazondata, table_name)
    if existed_days >= valid_days:
        return True

    return False

def delete_zombie_tables(sqlmgr):
    sale_count = 0
    sql = 'SHOW TABLES LIKE \'SALE\_%\''
    cursor = sqlmgr.ad_sale_data.query(sql)
    if cursor is not False:
        table_name_array = cursor.fetchall()
        for index in range(len(table_name_array)):
            table_name = table_name_array[index][0]
            asin = table_name.split('_')[1]
            if is_sale_asin(sqlmgr, asin) is False:
                sql = 'drop table ' + 'SALE_' + asin
                # print(sql, flush=True)
                sale_count += 1
                # sqlmgr.ad_sale_data.query(sql)

    inventory_count = 0
    sql = 'SHOW TABLES LIKE \'INVENTORY\_%\''
    cursor = sqlmgr.ad_sale_data.query(sql)
    if cursor is not False:
        table_name_array = cursor.fetchall()
        for index in range(len(table_name_array)):
            table_name = table_name_array[index][0]
            asin = table_name.split('_')[1]
            if is_sale_asin(sqlmgr, asin) is False:
                sql = 'drop table ' + 'INVENTORY_' + asin
                # print(sql, flush=True)
                inventory_count += 1
                # sqlmgr.ad_sale_data.query(sql)

    sql = 'SHOW TABLES'
    cursor = sqlmgr.ad_sale_data.query(sql)
    if cursor is not False:
        table_name_array = cursor.fetchall()
        print("total tables + " + str(len(table_name_array)), flush=True)

    print("delete zombie sale table + " + str(sale_count), flush=True)
    print("delete zombie inventory table + " + str(inventory_count), flush=True)

def delete_unused_tables(amazondata, table_name_condition, condition):
    if table_name_condition == False:
        sql = 'SHOW TABLES'
    else:
        sql = 'SHOW TABLES LIKE ' + table_name_condition # '\'%\_BS\''
    count = 0
    cursor = amazondata.query(sql)
    if cursor != False:
        result = cursor.fetchall()
        for index in range(len(result)):
            table_name = result[index][0]
            if is_table_expired(amazondata, table_name, 4):
                data = get_all_data(amazondata, table_name, False, condition)
                if data == False:
                    asin_array = get_all_data(amazondata, table_name, 'asin', 'limited=\'no\'')
                    if asin_array is not False:
                        for i in range(len(asin_array)):
                            sql = 'drop table ' + 'SALE_' + asin_array[i][0]
                            # print(sql, flush=True)
                            # amazondata.query(sql)
                            sql = 'drop table ' + 'INVENTORY_' + asin_array[i][0]
                            # print(sql, flush=True)
                            # amazondata.query(sql)
                            count += 2

                    delete_sql = 'drop table ' + result[index][0]
                    # print(delete_sql, flush=True)
                    count += 1
                    # amazondata.query(delete_sql)
    else:
        print("get all table in failure.. + " + amazondata.db_name, flush=True)

    print("delete_unused_tables + " + str(count), flush=True)
    return False


def get_all_table(amazondata, condition):
    table_array = []

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
        print("get all table in failure.. + " + amazondata.db_name, flush=True)

    if len(table_array) != 0:
        # print(table_array)
        return table_array

    return False

def get_node_name(amazondata, table_name, node):
    sql = 'select * from ' + table_name + ' where node=\'' + node + '\''
    cursor = amazondata.query(sql)
    if cursor != False:
        if cursor.rowcount > 0:
            result = cursor.fetchall()
            # print(result)
            return result

    return False


def get_node_name_from_all(amazondata, node):
    if amazondata.country == 'us':
        node_table_array = xls_file_array_us
    elif amazondata.country == 'jp':
        node_table_array = xls_file_array_jp

    for node_table in node_table_array:
        result = get_node_name(amazondata, node_table, node)
        if result != False:
            return result[0][1]

    return False

def get_all_data(amazondata, table_name, column, condition):
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

    return False

def delete_unused_node_task(sqlmgr, condition):
    if sqlmgr.country == 'jp':
        task_table = amazonglobal.table_sale_task_jp
    elif sqlmgr.country == 'us':
        task_table = amazonglobal.table_sale_task_us

    count = 0
    node_array = get_all_data(sqlmgr.ad_sale_task, task_table, 'node', False)
    for index in range(len(node_array)):
        table_name = node_array[index][0] + '_BS'
        if is_table_expired(sqlmgr.ad_sale_data, table_name, 4):
            data = get_all_data(sqlmgr.ad_sale_data, table_name, False, condition)
            if data == False:
                sql = 'delete from ' + task_table + ' where node=\'' + node_array[index][0] + '\''
                # status = sqlmgr.ad_sale_task.query(sql)
                # if status is False:
                #     print(" delete node in failure", flush=True)
                # else:
                count += 1

    print("delete_unused_node_task + " + str(count), flush=True)

def gather_sale_asin(sqlmgr):
    count = 0
    if sqlmgr.country == 'us':
        table_sale_task = amazonglobal.table_sale_task_us
    elif sqlmgr.country == 'jp':
        table_sale_task = amazonglobal.table_sale_task_jp
    node_array = get_all_data(sqlmgr.ad_sale_task, table_sale_task, 'node', False)
    if node_array is not False:
        for index in range(len(node_array)):
            table_name = node_array[index][0] + '_BS'
            data = get_all_data(sqlmgr.ad_sale_data, table_name, 'asin', 'price>=12 and limited<>\'yes\' and seller<4')
            if data is not False:
                for i in range(len(data)):
                    status = sqlmgr.ad_sale_task.create_sale_asin_table(amazonglobal.table_sale_asin_us)
                    if status is False:
                        print("create table in failure", flush=True)
                    else:
                        asin_data = {
                            'asin': data[i][0]
                        }
                        status = sqlmgr.ad_sale_task.insert_sale_asin_data(amazonglobal.table_sale_asin_us, asin_data)
                        if status is False:
                            print("insert sale asin data in failure", flush=True)
                        else:
                            count += 1

    print("gather_sale_asin + " + str(count), flush=True)

def is_sale_asin(sqlmgr, asin):
    if sqlmgr.country == 'us':
        table_sale_asin = amazonglobal.table_sale_asin_us
    elif sqlmgr.country == 'jp':
        table_sale_asin = amazonglobal.table_sale_asin_jp
    sql = 'select * from ' + table_sale_asin + ' where asin=\'' + asin + '\''
    cursor = sqlmgr.ad_sale_task.query(sql)
    if cursor != False:
        if cursor.rowcount > 0:
            return True

    return False

def update_asin_status_ok(amazondata, node):
    asin_array = get_all_data(amazondata, (node + '_BS'), 'asin', False)
    if asin_array != False:
        for index in range(len(asin_array)):
            condition = 'asin=\'' + asin_array[index][0] + '\'' + ' and status=\'err\''
            amazondata.update_data(node + '_BS', 'status', '\'ok\'', condition)


def update_asin_date(amazondata, node):
    today = date.today()
    condition = 'inventory_date=\'' + today.strftime("%Y-%m-%d") + '\''
    asin_array = get_all_data(amazondata, (node + '_BS'), 'asin', condition)
    if asin_array != False:
        for index in range(len(asin_array)):
            inventory_table_name = 'INVENTORY_' + asin_array[index][0]
            yesterday_inventory = amazondata.get_yesterday_inventory(inventory_table_name)
            today_inventory = amazondata.get_today_inventory(inventory_table_name)
            if today_inventory != 0:
                if (yesterday_inventory / today_inventory) > 10:
                    print("today inventory may error + " + asin_array[index][0], flush=True)
                    yesterday = date.today() + timedelta(days=-1)
                    condition = 'asin=\'' + asin_array[index][0] + '\''
                    amazondata.update_data(node + '_BS', 'inventory_date', '\'' + yesterday.strftime("%Y-%m-%d") + '\'', condition)


def fix_asin_sale(amazondata, node, err_sale_value):
    condition = 'avg_sale>0'
    asin_array = get_all_data(amazondata, (node + '_BS'), 'asin', condition)
    if asin_array != False:
        for index in range(len(asin_array)):
            sale_table_name = 'SALE_' + asin_array[index][0]
            amazondata.update_data(sale_table_name, 'sale', 0, 'sale>' + err_sale_value)
            avg_sale = amazondata.get_column_avg(sale_table_name, 'sale')
            if avg_sale is False:
                print("get column avg in failure..", flush=True)
            else:
                condition = 'asin=\'' + asin_array[index][0] + '\''
                amazondata.update_data(node + '_BS', 'avg_sale', int(avg_sale), condition)


def update_all_task_status(amazondata, table, country):
    condition = False # 'length(node)>4'
    node_array = get_all_data(amazondata, table, 'node', condition)
    for index in range(len(node_array)):
        if country == 'jp':
            update_asin_status_ok(amazondata, node_array[index][0])
        elif country == 'us':
            update_asin_status_ok(amazondata, node_array[index][0])


def update_all_task_date_status(sqlmgr, date, err_sale_value):
    if sqlmgr.country == 'jp':
        task_table = amazonglobal.table_sale_task_jp
    elif sqlmgr.country == 'us':
        task_table = amazonglobal.table_sale_task_us

    node_array = get_all_data(sqlmgr.ad_sale_task, task_table, 'node', False)
    for index in range(len(node_array)):
        # print(asin_array[index])
        condition = 'node=\'' + node_array[index][0] + '\''
        sqlmgr.ad_sale_task.update_data(task_table, 'last_date', '\'' + date + '\'', condition)
        sqlmgr.ad_sale_task.update_data(task_table, 'status', '\'' + 'ok' + '\'', condition)
        update_asin_status_ok(sqlmgr.ad_sale_data, node_array[index][0])
        update_asin_date(sqlmgr.ad_sale_data, node_array[index][0])
        fix_asin_sale(sqlmgr.ad_sale_data, node_array[index][0], err_sale_value)


def update_all_rank_task_date_status(date, sqlmgr):
    if sqlmgr.country == 'jp':
        task_table = amazonglobal.table_rank_task_jp
    elif sqlmgr.country == 'us':
        task_table = amazonglobal.table_rank_task_us

    id_array = get_all_data(sqlmgr.ad_rank_task, task_table, 'id', False)
    for index in range(len(id_array)):
        # print(asin_array[index])
        condition = 'id=' + str(id_array[index][0])
        sqlmgr.ad_rank_task.update_data(task_table, 'last_date', '\'' + date + '\'', condition)
        sqlmgr.ad_rank_task.update_data(task_table, 'status', '\'' + 'ok' + '\'', condition)

def count_pending_asin(sqlmgr, top_tpye):
    count = 0
    if sqlmgr.country == 'us':
        table_sale_task = amazonglobal.table_sale_task_us
    elif sqlmgr.country == 'jp':
        table_sale_task = amazonglobal.table_sale_task_jp
    sale_task_array = get_all_data(sqlmgr.ad_sale_task, table_sale_task, 'node', False)
    if sale_task_array is False:
        print("get all data in failure " + table_sale_task, flush=True)
    else:
        for index in range(len(sale_task_array)):
            node = sale_task_array[index][0]
            node_table_name = node + '_' + top_tpye
            condition = 'limited<>\'yes\' and seller<4 and price >= 12'
            pending_asin_array = get_all_data(sqlmgr.ad_sale_data, node_table_name, 'asin', condition)
            if pending_asin_array is False:
                print("get all data in failure " + node_table_name, flush=True)
            else:
                count += len(pending_asin_array)

    print("Total Pending Asins is " + str(count), flush=True)


def copy_table_data(from_amazondata, to_amazondata):
    data_array = get_all_data(from_amazondata, 'sale_task_us', False, False)
    if data_array is not False:
        for data in data_array:
            task_data = {
                'node': data[0],
                'status': data[1],
                'last_date': data[2],
                'node_name':data[3]
            }
            status = to_amazondata.insert_task_data('sale_task_us', task_data)
            if status is False:
                print("insert task data in failure.", flush=True)


# SELECT CREATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='amazondata' AND TABLE_NAME='INVENTORY_B07GYTTF8B';
if __name__ == "__main__":
    sqlmgr = SqlMgr('us')
    if sqlmgr.start() == False:
        print("SqlMgr initialized in failure", flush=True)
        exit()
    # amazondata = AmazonData()
    # status = amazondata.connect_database('amazondata')
    # if status == False:
    #     print("connect in failure..", flush=True)
    # else:
    #     pass
    # get_all_table('amazondata', '_BS')
    # get_all_data('amazondata', '2201158051_BS', False)
    # update_asin_status_ok('data_us', '165795011')
    # update_all_task_date('amazontask', '2018-10-06')
    # insert_all_node_info()
    # insert_all_ip_info('../myproxy.txt')
    # update_all_task_status()
    # get_all_node_name()
    # update_click_data('amkiller', 'tree swing', 'B0746QS8T2')
    # insert_all_node_info(sqlmgr.ad_node_info, xls_file_array_us)
    # delete_column('node_info_us', 'sporting_goods', 'status')
    # add_new_column(sqlmgr.ad_node_info, 'health', 'status', 'status VARCHAR(5) default \'no\' check(status in(\'no\', \'run\', \'yes\', \'err\'))')
    # delete_column('node_info_us', 'automotive', 'status')
    # update_all_task_status('amazontask', 'sale_task_us', 'us')
    # get_one_data('node_info_us', 'automotive', False)
    # delete_sale_task('us', 'task_delete.txt')
    # print(get_days_array_of_day(7, -1), flush=True)
    # print(get_days_array_of_day(2, 1), flush=True)

    # add_new_column('data_us', '_BS', 'seller_name', 'seller_name CHAR(20) NOT NULL default \'\'')
    # add_new_column('data_us', '_BS', 'size', 'size CHAR(30) NOT NULL default \'\'')
    # add_new_column('data_us', '_BS', 'weight', 'weight FLOAT(10) NOT NULL default 0')
    # seller_name = get_one_data(amazonglobal.db_name_data_us, '9977442011_BS', 'asin=' + '\'' + 'B01EHSX28M' + '\'')
    # print(seller_name[16], flush=True)
    # delete_unused_tables(sqlmgr.ad_sale_data, '\'%\_BS\'', 'avg_sale>5 and price>=12 and limited=\'no\'')
    # count_pending_asin(sqlmgr, 'BS')
    # copy_table_data(sqlmgr.ad_sale_data, sqlmgr.ad_sale_task)
    # get_table_existed_time(sqlmgr.ad_sale_data, 'GWA_BS')


    gather_sale_asin(sqlmgr)
    delete_unused_node_task(sqlmgr, 'avg_sale>5 and price>=12 and limited = \'no\'')
    delete_unused_tables(sqlmgr.ad_sale_data, '\'%\_BS\'', 'avg_sale>5 and price>=12 and limited=\'no\'')
    delete_zombie_tables(sqlmgr)

    sqlmgr.stop()
