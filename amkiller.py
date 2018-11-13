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
from amazonsearchpage import  AmazonSearchPage
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import utils
import pyautogui
import amazonwrapper
from sqlmgr import SqlMgr
from selenium import webdriver


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    amkillerfile = sys.argv[1]
    country = sys.argv[2]
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
    while count < 1:
    # while admin.is_all_over() == False:
        ret = utils.generate_info_file(ips_array)
        if ret == False:
            continue
        keyword = admin.get_random_task()
        if keyword == False:
            exit(-1)
        whiteasin = admin.get_whiteasin(keyword)
        blackasin = admin.get_blackasin(keyword)

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
        t1 = time.time()
        amazonpage = AmazonPage(driver)
        try:
            tmp = random.randint(1, 100)
            if tmp < 200: #30:
                ## registeration
                print(("* Registeration..."), flush=True)
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 200: #10:
                    ## add bill address
                    print(("* Add Bill Address..."), flush=True)
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                    tmp = random.randint(1, 100)
                    if tmp < 200: #10:
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
            searchpage.click_random_products(admin, keyword, blackasin, whiteasin)
            admin.finish_task(keyword)
            t2 = time.time()
            print("Total Time：" + format(t2 - t1), flush=True)
            time.sleep(random.randint(int(min_time), int(max_time)))
        except NoSuchElementException as msg:
            print(("* NoSuchElementException...."), flush=True)
        except TimeoutException as msg:
            print(("* Loaded Timeout...."), flush=True)
        except:
            pass
        finally:
            driver.quit()

        count += 1

    sqlmgr.stop()
