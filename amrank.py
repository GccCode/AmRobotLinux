#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time
import sys
from selenium import webdriver
from amazonpage import AmazonPage
from amazonsearchpage import  AmazonSearchPage
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from amazondata import AmazonData
import amazonglobal
from amazonwrapper import *


def customized_broswer():
    option = webdriver.ChromeOptions()
    # index = random.randint(0, (len(useragentlist) - 1))
    # useragent = "--user-agent=" + useragentlist[index]
    # option.add_argument(useragent)
    # option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    #
    # option.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    # option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # option.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    driver =  webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    driver.maximize_window()
    return driver

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # cf = configparser.ConfigParser()
    # cf.read("task.txt")

    driver = customized_broswer()
    amazondata = AmazonData()
    t1 = time.time()
    try:
        amazonpage = AmazonPage(driver)
        driver.get('https://www.amazon.com')
        amazonpage.wait_searchbox_exsist()
        searchpage = AmazonSearchPage(driver)
        # asinresult = False
        #entry_type = "sponsored"
        entry_type = "normal"
        keyword = "swing swivel"
        #asin = "B01HWSQIGM"
        #asin = "B075C6G6M1"
        asin = "B015OXL2MW"
        print(("start search keyword"), flush=True)
        amazonpage.search_asin(keyword, 8000, 10000)
        asinresult = searchpage.find_target_product_rank(asin, entry_type, int(5))
        if asinresult != False:
            db_name_rank_data = amazonglobal.db_name_rank_data_us
            table_rank_data = amazonglobal.table_rank_data_us
            status = update_rank_data(db_name_rank_data, table_rank_data, keyword, asinresult)
            if status == False:
                pass
            else:
                pass
        else:
            print(("can't find the asin"), flush=True)
    except NoSuchElementException as msg:
        print(("can't find the element"), flush=True)
    except TimeoutException as msg:
        print(("page loaded timeout"), flush=True)
    except:
        print(("unknown error"), flush=True)
    finally:
        t2 = time.time()
        print("总耗时：" + format(t2 - t1))
        input("xxxxxx")
        driver.quit()
