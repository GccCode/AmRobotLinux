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

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    amkillerfile = cf.get("configfile", "amkiller")
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")

    admin = utils.Administrator(amkillerfile)
    count = 0
    print("* resolution：" + str(pyautogui.size()))
    while count < 1:#admin.is_all_over() == False:
        ret = utils.generate_info_file()
        if ret == False:
            continue
        keyword = admin.get_random_task()
        whiteasin = admin.get_whiteasin(keyword)
        blackasin = admin.get_blackasin(keyword)
        driver = utils.customized_broswer()
        t1 = time.time()
        amazonpage = AmazonPage(driver)
        try:
            random.randint(1, 100)
            if count < 50:
                ## registeration
                print(("* Registeration..."), flush=True)
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 30:
                    ## add bill address
                    print(("* Add Bill Address..."), flush=True)
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                    tmp = random.randint(1, 100)
                    if tmp < 30:
                        ## add payment
                        print(("* Add Card..."), flush=True)
                        amazonpage.enter_account_page(3000, 5000)
                        accountpage = AmazonAccountPage(driver)
                        accountpage.enter_payment_page(3000, 5000)
                        paymentpage = AmazonPaymentPage(driver)
                        paymentpage.add_new_payment(5000, 10000)

            amazonpage.enter_amazon_page(3000, 5000)
            amazonpage.wait_searchbox_exsist()
            searchpage = AmazonSearchPage(driver)
            print(("* Start Search Keyword...."), flush=True)
            amazonpage.search_asin(keyword, 5000, 8000)
            asins = searchpage.click_random_products(blackasin, whiteasin)
            admin.record_tasks(keyword, asins)
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

    print("* Task Finished...")

