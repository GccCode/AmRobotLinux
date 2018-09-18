#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import string
import time
import requests
import sys
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re
import configparser
from selenium import webdriver
from amazonpage import AmazonPage
from amazonregisterpage import AmazonRegisterPage
from amazonaccountpage import AmazonAccountPage
from amazonaddresspage import AmazonAddressPage
from amazonpaymentpage import AmazonPaymentPage
from amazonsearchpage import  AmazonSearchPage
from amazonasinpage import  AmazonAsinPage
import os
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import utils


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    amtaskfile = cf.get("configfile", "amtask")
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")

    admin = utils.Administrator(amtaskfile)

    while admin.is_all_over() == False:
        utils.generate_info_file()
        task = admin.get_random_task()
        driver = utils.customized_broswer()
        t1 = time.time()
        try:
            amazonpage = AmazonPage(driver)
            ## registeration
            amazonpage.enter_amazon_page(3000, 5000)
            amazonpage.enter_register_page(3000, 5000)
            registerpage = AmazonRegisterPage(driver)
            registerpage.register(5000, 10000)
            ## add bill address
            amazonpage.enter_account_page(3000, 5000)
            accountpage = AmazonAccountPage(driver)
            accountpage.enter_address_page(3000, 5000)
            addresspage = AmazonAddressPage(driver)
            addresspage.add_address("bill", 5000, 10000)
            ## add payment
            amazonpage.enter_account_page(3000, 5000)
            accountpage = AmazonAccountPage(driver)
            accountpage.enter_payment_page(3000, 5000)
            paymentpage = AmazonPaymentPage(driver)
            paymentpage.add_new_payment(5000, 10000)

            amazonpage.enter_amazon_page(3000, 5000)

            searchpage = AmazonSearchPage(driver)
            searchpage_handle = 0
            asinresult = False
            entry_type = ""
            link = admin.is_super_link(task)
            if link != "0":
                print(("* Start To View The Product By SuperUrl..."), flush=True)
                amazonpage.enter_super_link(link, 3000, 5000)
                searchpage_handle = amazonpage.get_currenthandle()
                asinresult = True
            else:
                keyword = admin.get_keyword(task)
                print(("* Start To Search Keyword " + keyword), flush=True)
                amazonpage.search_asin(keyword, 5000, 8000)
                searchpage_handle = amazonpage.get_currenthandle()
                asinresult = searchpage.find_target_product(task, "normal", int(5))
                if asinresult != False:
                    searchpage.enter_asin_page(asinresult, task, 3000, 5000)

            if asinresult != False:
                print(("* Start To View The Product By Searching.."), flush=True)
                #amazonpage.random_walk(random.randint(35, 50))
                time.sleep(random.randint(10, 30))
                asinpage = AmazonAsinPage(driver)
                searchpage.switch_to_new_page(searchpage_handle)  # 切换到产品页handle

                qa_submit = admin.is_qa_submit_needed(task)
                if qa_submit == "1":
                    print(("* Start To Submit QA...."), flush=True)
                    content = admin.get_qa_content(task)
                    asinpage.ask_qa(content, 3000, 5000)
                    if admin.is_qa_submit_image(task) == "1":
                        amazonpage.window_capture("qa" + "-" + task)
                    amazonpage.navigation_back(3000, 5000)

                addcart = admin.is_add_to_card_needed(task)
                if addcart == "1":
                    print(("* Start To Add Cart..."), flush=True)
                    asinpage.add_cart(3000, 5000)
                    amazonpage.navigation_back(3000, 5000)
                else:
                    possible = random.randint(1, 100)
                    if possible < 70:
                        asinpage.add_cart(3000, 5000)
                        amazonpage.navigation_back(3000, 5000)

                wishlist = admin.is_add_wishlist_needed(task)
                if wishlist == "1":
                    print(("* Start To Add Wishlist..."), flush=True)
                    if admin.is_add_wishlist_image(task) == "1":
                        asinpage.add_wishlist(5000, 8000, task)
                    else:
                        asinpage.add_wishlist(5000, 8000)
                else:
                    possible = random.randint(1, 100)
                    if possible < 70:
                        asinpage.add_wishlist(5000, 8000)

                #searchpage.back_prev_page_by_country(searchpage_handle, 3000, 5000)

                admin.finish_task(task)
                time.sleep(random.randint(min_time, max_time))
            else:
                print(("Can't find the product..."), flush=True)
        except NoSuchElementException as msg:
            print(("* Can't find the element..."), flush=True)
        except TimeoutException as msg:
            print(("* Loaded Timeout..."), flush=True)
        except:
            pass
        finally:
            t2 = time.time()
            print("总耗时：" + format(t2 - t1))
            driver.quit()

    print("* 任务全部完成！！！！")

