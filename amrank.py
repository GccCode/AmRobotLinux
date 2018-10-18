#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from amazonpage import AmazonPage
from amazonsearchpage import  AmazonSearchPage
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import amazonglobal
import amazonwrapper
import utils
from datetime import date
import traceback


def get_rank_data(ips_array, country, asin, keyword, entry_type):
    try:
        driver = utils.customized_broswer_with_luminati(ips_array)
        status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'no')
        if status == False:
            print("update rank task status in failure..", flush=True)
        amazonpage = AmazonPage(driver)
        if country == 'us':
            driver.get('https://www.amazon.com')
        elif country == 'jp':
            driver.get('https://www.amazon.co.jp')
        amazonpage.wait_searchbox_exsist()
        searchpage = AmazonSearchPage(driver)

        print(("start search keyword"), flush=True)
        amazonpage.search_asin(keyword, 8000, 10000)
        asinresult = searchpage.find_target_product_rank(asin, entry_type, int(5))
        if asinresult != False:
            db_name_rank_data = amazonglobal.db_name_rank_data_us
            table_rank_data = amazonglobal.table_rank_data_us
            status = amazonwrapper.update_rank_data(db_name_rank_data, table_rank_data, keyword, asinresult)
            if status == False:
                print("update rank data in failure..", flush=True)
            else:
                status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'ok')
                if status == False:
                    print("update rank task status in failure..", flush=True)
        else:
            print(("can't find the asin"), flush=True)
            status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'ok')
            if status == False:
                print("update rank task status in failure..", flush=True)
    except NoSuchElementException as msg:
        print(("can't find the element"), flush=True)
        status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'ok')
        if status == False:
            print("update rank task status in failure..", flush=True)
    except TimeoutException as msg:
        print(("page loaded timeout"), flush=True)
        status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'ok')
        if status == False:
            print("update rank task status in failure..", flush=True)
    except:
        print(("unknown error"), flush=True)
        status = amazonwrapper.update_rank_task_status(country, keyword, entry_type, 'ok')
        if status == False:
            print("update rank task status in failure..", flush=True)
    finally:
        if driver != False:
            driver.quit()

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    country = sys.argv[1]
    ips_array = amazonwrapper.get_all_accessible_ip(country)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)

    if country == 'us':
        task_table = amazonglobal.table_rank_task_us
    elif country == 'jp':
        task_table = amazonglobal.table_rank_task_jp

    try:
        cur_date = date.today()
        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
        status_condition = 'status<>\'no\' and last_date<>' + value
        rank_task = amazonwrapper.get_one_data(amazonglobal.db_name_rank_task, task_table, status_condition)
        while rank_task != False:
            asin = rank_task[1]
            keyword = rank_task[2]
            entry_type = rank_task[3]
            print(asin, flush=True)
            print(keyword, flush=True)
            print(entry_type, flush=True)
            get_rank_data(ips_array, country, asin, keyword, entry_type)
            rank_task = amazonwrapper.get_one_data(amazonglobal.db_name_rank_task, task_table, status_condition)
    except:
        print(traceback.format_exc(), flush=True)

