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
from amazonasinpage import  AmazonAsinPage
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import utils
import amazonwrapper


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    amtaskfile = cf.get("configfile", "amtask")
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")
    page = cf.get("search", "page")
    country = sys.argv[1]
    ips_array = amazonwrapper.get_all_accessible_ip(country)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    admin = utils.Administrator(amtaskfile)

    while admin.is_all_over() == False:
        utils.generate_info_file(ips_array)
        task = admin.get_random_task()
        driver = utils.customized_broswer_with_luminati(ips_array)
        t1 = time.time()
        try:
            login_flag = False
            possible = random.randint(1, 100)
            amazonpage = AmazonPage(driver)
            if possible > 40 or admin.is_login_required(task):
                ## registeration
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                login_flag = True
                possible = random.randint(1, 100)
                ## add bill address
                if possible > 70:
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                    possible = random.randint(1, 100)
                    if possible > 70:
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
                print(task, flush=True)
                asinresult = searchpage.find_target_product(task, "normal", int(page) + 1)
                if asinresult != False:
                    searchpage.enter_asin_page(asinresult, task, 3000, 5000)
                    searchpage.random_walk(random.randint(10, 20))

            if asinresult != False:
                print(("* Start To View The Product By Searching.."), flush=True)
                #amazonpage.random_walk(random.randint(35, 50))
                time.sleep(random.randint(10, 30))
                asinpage = AmazonAsinPage(driver)
                searchpage.switch_to_new_page(searchpage_handle)  # 切换到产品页handle

                qa_submit = admin.is_qa_submit_needed(task)
                if qa_submit == "1" and login_flag:
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
                if wishlist == "1" and login_flag:
                    print(("* Start To Add Wishlist..."), flush=True)
                    if admin.is_add_wishlist_image(task) == "1":
                        asinpage.add_wishlist(5000, 8000, task)
                    else:
                        asinpage.add_wishlist(5000, 8000, False)
                else:
                    possible = random.randint(1, 100)
                    if possible < 70:
                        asinpage.add_wishlist(5000, 8000, task)

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

