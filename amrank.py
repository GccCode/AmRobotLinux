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
from selenium import webdriver


def get_rank_data(ips_array, sqlmgr, asin, keyword, entry_type, page):
    status = True
    try:
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        user_prefix = 'lum-customer-hl_ecee3b35-zone-shared_test_api-ip-'
        ip = amazonwrapper.get_ramdon_accessible_ip(ips_array)
        if ip == False:
            print("can't get accessible ip", flush=True)
            exit(-1)
        proxyauth_plugin_path = utils.create_proxyauth_extension(
            proxy_host='zproxy.lum-superproxy.io',
            proxy_port=22225,
            proxy_username=user_prefix + ip,
            proxy_password='o9dagiaeighm'
        )
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_extension(proxyauth_plugin_path)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        # driver = utils.customized_broswer_with_luminati(ips_array)
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

            asinresult = searchpage.find_target_product_rank(asin, entry_type, page)
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
                status = amazonwrapper.update_rank_data(sqlmgr.ad_rank_data, table_rank_data, keyword, entry_type, [20, 50])
                if status == False:
                    print("update rank data in failure..", flush=True)
                else:
                    status = amazonwrapper.update_rank_task_date(sqlmgr.ad_rank_task, keyword, entry_type)
                    if status == False:
                        print("update rank task date in failure..", flush=True)
    except NoSuchElementException as msg:
        status = False
        print(("can't find the element"), flush=True)
    except TimeoutException as msg:
        status = False
        print(("page loaded timeout"), flush=True)
    except:
        status = False
        print(("unknown error"), flush=True)
    finally:
        if driver != False:
            driver.quit()
        if status is not False:
            status = amazonwrapper.update_rank_task_run_status(sqlmgr.ad_rank_task, keyword, entry_type, 'ok')
            if status == False:
                print("update rank task status in failure..", flush=True)

def is_keyword_rank_unavailable(sqlmgr, keyword, type):
    cur_date = date.today().strftime("%Y_%m_%d")
    if sqlmgr.country == 'us':
        task_table = 'task_us'
    elif sqlmgr.country == 'jp':
        task_table = 'task_jp'
    status = 'keyword = \'' + keyword + '\' and type = \'' + type + '\''
    rank = amazonwrapper.get_all_data(sqlmgr.ad_rank_data, task_table, cur_date, status)
    print(rank, flush=True)
    if rank is not False:
        if rank[0][0] == '2050':
            return True
        else:
            return False
    else:
        return True

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
            is_flush = sys.argv[3]
            if is_flush == '1':
                yesterday = date.today() + timedelta(days=-1)
                amazonwrapper.update_all_rank_task_date_status(yesterday.strftime("%Y-%m-%d"), sqlmgr)
            is_specificed = sys.argv[4]
            if is_specificed == '0':
                status_condition = 'status<>\'no\' and last_date<>' + value
            else:
                status_condition = is_specificed
            rank_task = amazonwrapper.get_one_data(sqlmgr.ad_rank_task, task_table, status_condition)
            while rank_task != False:
                asin = rank_task[2]
                keyword = rank_task[3]
                entry_type = rank_task[4]
                if rank_task[5] == 0:
                    page = 5
                else:
                    page = rank_task[5]
                # print(asin, flush=True)
                print(keyword, flush=True)
                # print(entry_type, flush=True)
                for i in range(3):
                    if is_keyword_rank_unavailable(sqlmgr, keyword, entry_type):
                        get_rank_data(ips_array, sqlmgr, asin, keyword, entry_type, page)
                rank_task = amazonwrapper.get_one_data(sqlmgr.ad_rank_task, task_table, status_condition)
    except:
        print(traceback.format_exc(), flush=True)

    sqlmgr.stop()

