#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pymysql
import configparser

class AmazonSql():
    def __init__(self, filename):
        self.cf = configparser.ConfigParser()
        self.cf.read(filename)
        self.host = self.cf.get("logininfo", "host")
        self.user = self.cf.get("logininfo", "user")
        self.password = self.cf.get("logininfo", "password")
        self.port = int(self.cf.get("logininfo", "port"))

    def connect_sql(self, db_name):
        db = None
        try:
            if db_name == "False":
                db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port)
            else:
                db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=db_name)
        except Exception as e:
            print(str(e), flush=True)
            db = False
        finally:
            return db

    def is_mysql_table_exsist(self, db, table):
        result = False
        sql = 'show tables like \'' + table + '\''
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            if cursor.rowcount > 0:
                result = cursor
                # print("AmazonSql Table is exsist + " + table, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            db.rollback()
        finally:
            return result

    def is_mysql_database_exsist(self, db, db_name):
        result = False
        sql = 'show databases like \'' + db_name + '\''
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            if cursor.rowcount > 0:
                result = cursor
                # print("AmazonSql Database is exsist + " + db_name, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            db.rollback()
        finally:
            return result

    def is_mysql_column_exsit(self, db, db_name, table, column):
        result = False
        sql = 'SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'' + db_name + '\' AND table_name=\'' + table + '\'' + ' AND column_name=\'' + column + '\''
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            if cursor.rowcount > 0:
                result = cursor
                # print("AmazonSql Column is exsist + " + column, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            db.rollback()
        finally:
            return result


    def create_db(self, db, db_name):
        status = True
        try:
            cursor = db.cursor()
            sql = 'CREATE DATABASE ' + db_name + ' DEFAULT CHARACTER SET utf8'
            cursor.execute(sql)
        except Exception as e:
            print(str(e), flush=True)
            status = False
        finally:
            return status

    def create_table(self, db, table, columns):
        status = True
        try:
            cursor = db.cursor()
            sql = 'CREATE TABLE IF NOT EXISTS ' + table + ' (' + columns + ')'
            cursor.execute(sql)
        except Exception as e:
            print(str(e), flush=True)
            status = False
        finally:
            return status

    def query(self, db, sql):
        status = True
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            if 'delete' in sql or 'update' in sql:
                db.commit()
                status = True
            else:
                if cursor.rowcount > 0:
                    print(cursor.fetchall(), flush=True)
                    status = cursor
                else:
                    status = False
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def insert_data(self, db, table, data):
        # data = {
        #     'id': '20120001',
        #     'name': 'Bob',
        #     'age': 20
        # }
        status = True
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            cursor = db.cursor()
            # if cursor.execute(sql, tuple(data.values())):
            if cursor.execute(sql, tuple(data.values())*2):
                # print('AmazonSql Insert Sucessfully: ' + str(data))
                db.commit()
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def add_column(self, db, table, column):
        # 'ALTER TABLE TABLE_NAME ADD COLUMN NEW_COLUMN_NAME varchar(45) not null'
        status = True
        sql = 'ALTER TABLE ' + table + ' ADD COLUMN ' + column
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Add Column Sucessfully + " + column, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def modify_column(self, db, table, column):
        # 'ALTER TABLE TABLE_NAME ADD COLUMN NEW_COLUMN_NAME varchar(45) not null'
        status = True
        sql = 'ALTER TABLE ' + table + ' MODIFY COLUMN ' + column
        print(sql, flush=True)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Add Column Sucessfully + " + column, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def delete_column(self, db, table, column):
        # 'ALTER TABLE TABLE_NAME ADD COLUMN NEW_COLUMN_NAME varchar(45) not null'
        status = True
        sql = 'ALTER TABLE ' + table + ' DROP COLUMN ' + column
        print(sql, flush=True)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Add Column Sucessfully + " + column, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def update_data(self, db, table, key, value, condition):
        # 'UPDATE students SET age = %s WHERE name = %s'
        status = True
        sql = 'UPDATE {table} SET {key} = {value} WHERE {condition}'.format(table=table, key=key, value=value, condition=condition)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Update Data Sucessfully + " + key + ' ' + value + ' WHERE ' + condition, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def update_data_autoinc(self, db, table, key, condition):
        # 'UPDATE students SET age = %s WHERE name = %s'
        status = True
        sql = 'UPDATE ' + table + ' SET ' + key + '=' + key + '+1' + ' WHERE ' + condition
        # print(sql, flush=True)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Update Data Sucessfully + " + key + ' ' + value + ' WHERE ' + condition, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def update_data_autodes(self, db, table, key, condition):
        # 'UPDATE students SET age = %s WHERE name = %s'
        status = True
        sql = 'UPDATE ' + table + ' SET ' + key + '=' + key + '-1' + ' WHERE ' + condition
        # print(sql, flush=True)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # print("AmazonSql Update Data Sucessfully + " + key + ' ' + value + ' WHERE ' + condition, flush=True)
        except Exception as e:
            print(str(e), flush=True)
            status = False
            db.rollback()
        finally:
            return status

    def select_data(self, db, sql):
        # sql = 'SELECT * FROM students WHERE age >= 20'
        result = False
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            if cursor.rowcount > 0:
                result = cursor
                # print("AmazonSql Select Data Sucessfully ", flush=True)
        except Exception as e:
            print(str(e), flush=True)
            db.rollback()
        finally:
            return result

    def disconnect(self, db):
        db.close()


if __name__ == "__main__":
    amsql = AmazonSql("login.info")

    db = amsql.connect_sql('test')
    if db == False:
        print("Connect in failure..")
    else:
        print("Connect sucessfully..")
        status = amsql.is_mysql_table_exsist(db, 'amazon')
        if status != False:
            print((status.rowcount))
            result = status.fetchall()
            print(result[0][0])

    # status = amsql.update_data(db, 'amazon', 'age', '20', 'sex = \'male\'')
    # if status == False:
    #     print("failed")
    # else:
    #     print("cccccc")
    amsql.disconnect(db)
