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
from datetime import timedelta
import traceback
from sqlmgr import SqlMgr


def get_rank_data(ips_array, sqlmgr, asin, keyword, entry_type):
    try:
        driver = utils.customized_broswer_with_luminati(ips_array)
        status = amazonwrapper.update_rank_task_run_status(sqlmgr.ad_rank_task, keyword, entry_type, 'no')
        if status == False:
            print("update rank task status in failure..", flush=True)
        amazonpage = AmazonPage(driver)
        if sqlmgr.country == 'us':
            driver.get('https://www.amazon.com')
        elif sqlmgr.country == 'jp':
            driver.get('https://www.amazon.co.jp')
        status = amazonpage.wait_searchbox_exsist()
        if status == False:
            print("ip problems..", flush=True)
            return False
        searchpage = AmazonSearchPage(driver)

        print(("start search keyword"), flush=True)
        status = amazonpage.search_asin(keyword, 8000, 10000)
        if status != False:
            if sqlmgr.country == 'us':
                table_rank_data = amazonglobal.table_rank_data_us
            elif sqlmgr.country == 'jp':
                table_rank_data = amazonglobal.table_rank_data_jp

            asinresult = searchpage.find_target_product_rank(asin, entry_type, int(5))
            if asinresult != False:
                status = amazonwrapper.update_rank_data(sqlmgr.ad_rank_data, table_rank_data, keyword, entry_type, asinresult)
                if status == False:
                    print("update rank data in failure..", flush=True)
                else:
                    status = amazonwrapper.update_rank_task_date(sqlmgr.ad_rank_task, keyword, entry_type)
                    if status == False:
                        print("update rank task date in failure..", flush=True)

            else:
                print(("can't find the asin"), flush=True)
                status = amazonwrapper.update_rank_data(sqlmgr.ad_rank_data, table_rank_data, keyword, entry_type, [99, 99])
                if status == False:
                    print("update rank data in failure..", flush=True)
                else:
                    status = amazonwrapper.update_rank_task_date(sqlmgr.ad_rank_task, keyword, entry_type)
                    if status == False:
                        print("update rank task date in failure..", flush=True)
    except NoSuchElementException as msg:
        print(("can't find the element"), flush=True)
    except TimeoutException as msg:
        print(("page loaded timeout"), flush=True)
    except:
        print(("unknown error"), flush=True)
    finally:
        if driver != False:
            driver.quit()
        status = amazonwrapper.update_rank_task_run_status(sqlmgr.ad_rank_task, keyword, entry_type, 'ok')
        if status == False:
            print("update rank task status in failure..", flush=True)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    country = sys.argv[1]
    task_type = sys.argv[2]

    sqlmgr = SqlMgr(country)
    if sqlmgr.start() == False:
        print("SqlMgr initialized in failure", flush=True)
        exit()

    ips_array = amazonwrapper.get_all_accessible_ip(sqlmgr.ad_ip_info)
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
        if task_type == 'set':
            rank_file = sys.argv[3]
            amazonwrapper.insert_all_keyword_into_task(rank_file, sqlmgr)
        elif task_type == 'run':
            yesterday = date.today() + timedelta(days=-1)
            amazonwrapper.update_all_rank_task_date_status(yesterday.strftime("%Y-%m-%d"), sqlmgr)
            status_condition = 'status<>\'no\' and last_date<>' + value
            rank_task = amazonwrapper.get_one_data(sqlmgr.ad_rank_task, task_table, status_condition)
            while rank_task != False:
                asin = rank_task[2]
                keyword = rank_task[3]
                entry_type = rank_task[4]
                # print(asin, flush=True)
                print(keyword, flush=True)
                # print(entry_type, flush=True)
                get_rank_data(ips_array, sqlmgr, asin, keyword, entry_type)
                rank_task = amazonwrapper.get_one_data(sqlmgr.ad_rank_task, task_table, status_condition)
    except:
        print(traceback.format_exc(), flush=True)

    sqlmgr.stop()

