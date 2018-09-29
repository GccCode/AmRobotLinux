#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazondata import AmazonData
import xlrd
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
                  'toys']

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

def get_all_data(db_name, table_name):
    table_array = []
    amazondata = AmazonData()
    status = amazondata.connect_database(db_name)
    if status == False:
        print("connect in failure..", flush=True)
    else:
        sql = 'select * from ' + table_name
        cursor = amazondata.query(sql)
        if cursor != False:
            if cursor.rowcount > 0:
                result = cursor.fetchall()
                print(result)
                return result
        else:
            print("get all table in failure.. + " + db_name, flush=True)

        amazondata.disconnect_database()

    return False

# SELECT CREATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='amazondata' AND TABLE_NAME='INVENTORY_B07GYTTF8B';
if __name__ == "__main__":
    # amazondata = AmazonData()
    # status = amazondata.connect_database('amazondata')
    # if status == False:
    #     print("connect in failure..", flush=True)
    # else:
    #     pass
    # get_all_table('amazondata', '_BS')
    get_all_data('amazondata', '2201158051_BS')