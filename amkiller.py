#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time
import sys
import configparser
from amazonpage import AmazonPage
from amazonregisterpage import AmazonRegisterPage
from amazonaccountpage import AmazonAccountPage
from amazonaddresspage import AmazonAddressPage
from amazonpaymentpage import AmazonPaymentPage
from amazonasinpage import AmazonAsinPage
from amazonsearchpage import  AmazonSearchPage
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import utils
import pyautogui
import amazonwrapper
from sqlmgr import SqlMgr


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    amkillerfile = sys.argv[1]
    country = sys.argv[2]
    task_type = sys.argv[3] # 0: cpc clicker 1: fake traffic
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")

    sqlmgr = SqlMgr(country)
    if sqlmgr.start() == False:
        print("SqlMgr initialized in failure", flush=True)
        exit()

    admin = utils.Administrator(amkillerfile, sqlmgr)
    count = 0
    print("* Resolution：" + str(pyautogui.size()))
    ips_array = amazonwrapper.get_all_accessible_ip(sqlmgr.ad_ip_info)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    if task_type == '0':
        loop_status = (count < 1)
    else:
        loop_status = (admin.is_all_over() == False)
    while loop_status:
    # while admin.is_all_over() == False:
        ret = utils.generate_info_file(ips_array)
        if ret == False:
            continue
        keyword = admin.get_random_task()
        if keyword == False:
            exit(-1)
        whiteasin = admin.get_whiteasin(keyword)
        blackasin = admin.get_blackasin(keyword)

        driver = utils.customized_broswer_with_luminati(ips_array)
        t1 = time.time()
        amazonpage = AmazonPage(driver)
        asinresult = False
        try:
            register_flag = False
            tmp = random.randint(1, 100)
            if tmp < 30: #30:
                ## registeration
                print(("* Registeration..."), flush=True)
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                register_flag = True
                tmp = random.randint(1, 100)
                if tmp < 10: #10:
                    ## add bill address
                    print(("* Add Bill Address..."), flush=True)
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                    tmp = random.randint(1, 100)
                    if tmp < 10: #10:
                        ## add payment
                        print(("* Add Card..."), flush=True)
                        amazonpage.enter_account_page(3000, 5000)
                        accountpage = AmazonAccountPage(driver)
                        accountpage.enter_payment_page(3000, 5000)
                        paymentpage = AmazonPaymentPage(driver)
                        paymentpage.add_new_payment(5000, 10000)
            amazonpage.enter_amazon_page(30, 50)
            amazonpage.wait_searchbox_exsist()
            searchpage = AmazonSearchPage(driver)
            print(("* Start Search Keyword.... + " + keyword), flush=True)
            amazonpage.search_asin(keyword, 3000, 5000)
            if task_type == '0':
                searchpage.click_random_products(admin, keyword, blackasin, whiteasin)
            else:
                searchpage_handle = amazonpage.get_currenthandle()
                condition_setup = cf.get("search", "condition_setup")
                if condition_setup == "1":
                    input("请进行手动卡位，完成后按回车键继续自动搜索产品！！！")
                page = cf.get("search", "page")
                asin = cf.get("search", "asin")
                type = cf.get("search", "type")
                if type == "0":
                    entry_type = "sponsored"
                elif type == "1":
                    entry_type = "normal"

                asinresult = searchpage.find_target_product(asin, entry_type, (int(page) + 1))
                if asinresult != False:
                    fakeview = cf.get("search", "fakeview")
                    if fakeview == "1":
                        min_time = int(cf.get("search", "view_time_min"))
                        max_time = int(cf.get("search", "view_time_max"))
                        searchpage.enter_random_products(asin, random.randint(2, 3), min_time, max_time, 5000, 8000)
                    asinresult = searchpage.find_target_product(asin, entry_type, int(page))
                    if asinresult != False:
                        searchpage.enter_asin_page(asinresult, asin, 3000, 5000)
                    else:
                        print(("找不到产品！！！！"), flush=True)
                else:
                    print(("找不到产品！！！！"), flush=True)

                if asinresult != False:
                    variation_setup = cf.get("search", "variation_setup")
                    if variation_setup == "1":
                        input("请进行手动选择目标变体，完成后按回车键继续自动化！！！：")
                    mainview = cf.get("search", "mainview")
                    if mainview == "1":
                        print(("* 开始随意浏览产品页。。。"), flush=True)
                        min_time = int(cf.get("search", "mainview_time_min"))
                        max_time = int(cf.get("search", "mainview_time_max"))
                        amazonpage.random_walk(random.randint(min_time, max_time))
                        asinpage = AmazonAsinPage(driver)
                        searchpage.switch_to_new_page(searchpage_handle)  # 切换到产品页handle

                        tmp = random.randint(1, 100)
                        if tmp < 10 and register_flag is True:  # 10:
                            print(("* 开始添加wishlist。。。。"), flush=True)
                            asinpage.add_wishlist(5000, 8000, asin)

                        print(("* 开始加购物车。。。"), flush=True)
                        status = asinpage.add_cart(3000, 5000)
                        if status == False:
                            print("* 加购物车失败。。。", flush=True)

                        searchpage.back_prev_page_by_country(searchpage_handle, 3000, 5000)

                    random_status = random.randint(1, 200)
                    if (random_status % 2) == 1:
                        print(("* 随意浏览并等待退出"), flush=True)
                        amazonpage.random_walk(random.randint(2, 7))
            if (asinresult != False and task_type != '0') or task_type == '0':
                admin.finish_task(keyword)
            t2 = time.time()
            print("Total Time：" + format(t2 - t1), flush=True)
            time.sleep(random.randint(60, 800))
        except NoSuchElementException as msg:
            print(("* NoSuchElementException...."), flush=True)
        except TimeoutException as msg:
            print(("* Loaded Timeout...."), flush=True)
        except:
            pass
        finally:
            driver.quit()

        count += 1

        if task_type == '0':
            loop_status = (count < 1)
        else:
            loop_status = (admin.is_all_over() == False)

    sqlmgr.stop()
