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
from utils import change_random_resolution
import utils

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")
    admin = utils.Administrator()
    count = 0
    while admin.is_all_over() == False:
        change_random_resolution()
        utils.generate_info_file()
        keyword = admin.get_random_task()
        whiteasin = admin.get_whiteasin(keyword)
        driver = utils.customized_broswer()
        t1 = time.time()
        amazonpage = AmazonPage(driver)
        try:
            random.randint(1, 100)
            if count < 50:
                ## registeration
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 30:
                    ## add bill address
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 30:
                    ## add payment
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_payment_page(3000, 5000)
                    paymentpage = AmazonPaymentPage(driver)
                    paymentpage.add_new_payment(5000, 10000)

            amazonpage.enter_amazon_page(3000, 5000)
            amazonpage.wait_searchbox_exsist()
            searchpage = AmazonSearchPage(driver)
            print(("* 开始搜索关键词。。。"), flush=True)
            amazonpage.search_asin(keyword, 5000, 8000)
            searchpage.click_random_products(whiteasin)
            admin.finish_task(keyword)
            t2 = time.time()
            print("总耗时：" + format(t2 - t1))
            time.sleep(random.randint(int(min_time), int(max_time)))
        except NoSuchElementException as msg:
            print(("* 找不到元素。。。"), flush=True)
        except TimeoutException as msg:
            print(("* 网页加载超时。。。"), flush=True)
        except:
            pass
        finally:
            driver.quit()

        count += 1

    print("* 任务全部完成！！！！")

