#!/usr/bin/env python
# -*- coding:utf-8 -*-


from amazonpage import AmazonPage
from locator import AmazonSearchPageLocator
import configparser
import time as tm
import pyautogui
from selenium.common.exceptions import NoSuchElementException
import random


class AmazonSearchPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonSearchPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")
        self.screen_width = pyautogui.size()[0]
        self.screen_heigth = pyautogui.size()[1]

    def find_target_asin_rank(self, asin, type):
        index = 1
        asinresults = self.driver.find_elements(*self.locator.ASINRESULTS)
        for asinresult in asinresults:
            if asinresult.get_attribute('data-asin') == asin:
                if type == "normal":
                    if self.is_asin_sponsored(asinresult, asin) != True:
                        print(("** 找到目标产品 - 普通。。。"), flush=True)
                        return index
                elif type == "sponsored":
                    if self.is_asin_sponsored(asinresult, asin):
                        print(("** 找到目标产品 - 广告。。。"), flush=True)
                        return index
            else:
                index += 1

        return False

    def find_target_product_rank(self, asin, type, pages):
        print(("** 开始查找产品，限制页数：" + str(pages)), flush=True)
        task_cf = configparser.ConfigParser()
        task_cf.read("task.txt")
        for page in range(1, pages):
            asinresult = self.find_target_asin_rank(asin, type)
            if asinresult != False:
                print(("*** 目标页数：" + str(page)), flush=True)
                print(("*** 页面排名：" + str(asinresult)), flush=True)
                return [page, asinresult]
            else:
                self.enter_next_page(5000, 8000)
        return False

    def find_target_product(self, asin, type, pages):
        print(("** 开始查找产品，限制页数：" + str(pages)), flush=True)
        task_cf = configparser.ConfigParser()
        task_cf.read("task.txt")
        for page in range(1, pages):
            print(("*** 当前处于的页数是：" + str(page)), flush=True)
            asinresult = self.find_target_asin(asin, type)
            if asinresult != False:
                print(("*** 目标产品被找到的页数：" + str(page)), flush=True)
                return asinresult
            else:
                fakediff = task_cf.get("search", "fakediff")
                if fakediff == "1":
                    min_time = int(task_cf.get("search", "diff_time_min"))
                    max_time = int(task_cf.get("search", "diff_time_max"))
                    self.enter_random_products(False, random.randint(0, 2), min_time, max_time, 3000, 5000)
                self.enter_next_page(3000, 5000)
        return False

    def enter_random_products(self, asin, items, start_time, end_time, begin, end):
        #print("访问当前页面任意产品，数量为：" + str(count) + "\n")
        for i in range(0, items):
            self.enter_random_product(asin, random.randint(start_time, end_time), begin, end)

    def click_random_products(self, asin):
        count = 0
        limit = random.randint(1, 2)
        while count < limit:
            try:
                normal, sponsored = self.filter_asin(asin)
                normal_selected = []
                sponsored_selected = []
                if len(normal) != 0:
                    if len(normal) == 1:
                        normal_selected = random.sample(normal, 1)
                    else:
                        normal_selected = random.sample(normal, random.randint(1, 2))

                    for index in range(0, len(normal_selected)):
                        print(("*** 点击Normal产品：" + normal_selected[index].get_attribute('data-asin')), flush=True)
                        currenthandle = self.enter_asin_page(normal_selected[index], normal_selected[index].get_attribute('data-asin'), 10000, 15000)
                        self.back_prev_page_by_country(currenthandle, 3000, 5000)

                if len(sponsored) != 0:
                    if len(sponsored) == 1:
                        sponsored_selected = random.sample(sponsored, 1)
                    else:
                        sponsored_selected = random.sample(sponsored, random.randint(1, 2))

                    for index in range(0, (len(sponsored_selected) - 1)):
                        print(("*** 点击Sponsored产品：" + sponsored_selected[index].get_attribute('data-asin')), flush=True)
                        currenthandle = self.enter_asin_page(sponsored_selected[index], sponsored_selected[index].get_attribute('data-asin'), 20000, 35000)
                        self.back_prev_page_by_country(currenthandle, 3000, 5000)

                count += 1
                self.enter_next_page(3000, 5000)
            except:
                print(("*** unknown error!!!!"), flush=True)



    def enter_random_product(self, asin, count, begin, end):
        t1 = tm.time()
        index = 0
        asinresults = self.driver.find_elements(*self.locator.ASINRESULTS)
        if asin == False:
            tmp = random.randint(0, (len(asinresults) - 1))
            print(("*** 访问当前页面产品 + " + asinresults[tmp].get_attribute('data-asin')), flush=True)
            currenthandle = self.enter_asin_page(asinresults[tmp], asinresults[tmp].get_attribute('data-asin'), 3000, 5000)
            random_status = random.randint(1, 200)
            if (random_status % 2) == 1:
                self.random_walk(count)
            self.back_prev_page_by_country(currenthandle, begin, end)
        else:
            for asinresult in asinresults:
                if asinresult.get_attribute('data-asin') == asin:
                    tmp = random.randint(0, (len(asinresults) - 1))
                    # print("tmp = " + str(tmp) + "\n")
                    # print("index = " + str(index) + "\n")
                    while tmp == index:
                        tmp = random.randint(0, (len(asinresults) - 1))

                    print(("*** 访问当前页面除目标产品以外的产品 + " + asinresults[tmp].get_attribute('data-asin')), flush=True)
                    currenthandle = self.enter_asin_page(asinresults[tmp], asinresults[tmp].get_attribute('data-asin'), 3000, 5000)

                    random_status = random.randint(1, 200)
                    if (random_status % 2) == 1:
                        self.random_walk(count)
                    self.back_prev_page_by_country(currenthandle, begin, end)
                    break
                else:
                    index += 1

            t2 = tm.time()
            # print("random_mouse_move-总耗时：" + format(t2 - t1))

    def find_target_asin(self, asin, type):
        asinresults = self.driver.find_elements(*self.locator.ASINRESULTS)
        for asinresult in asinresults:
            if asinresult.get_attribute('data-asin') == asin:
                if type == "normal":
                    if self.is_asin_sponsored(asinresult, asin) != True:
                        print(("** 找到目标产品 - 普通。。。"), flush=True)
                elif type == "sponsored":
                    if self.is_asin_sponsored(asinresult, asin):
                        print(("** 找到目标产品 - 广告。。。"), flush=True)

                return asinresult

        return False

    def filter_asin(self, whiteasin):
        normal = []
        sponsored = []
        asinresults = self.driver.find_elements(*self.locator.ASINRESULTS)
        for asinresult in asinresults:
            if self.is_asin_sponsored(asinresult, asinresult.get_attribute('data-asin')) != True:
                print(("** 找到目标产品 - 普通。。。"), flush=True)
                if whiteasin != False:
                    if whiteasin != asinresult.get_attribute('data-asin'):
                        normal.append(asinresult)
                else:
                    normal.append(asinresult)
            elif self.is_asin_sponsored(asinresult, asinresult.get_attribute('data-asin')):
                print(("** 找到目标产品 - 广告。。。"), flush=True)
                if whiteasin != False:
                    if whiteasin != asinresult.get_attribute('data-asin'):
                        sponsored.append(asinresult)
                else:
                    sponsored.append(asinresult)

        return normal, sponsored


    def is_asin_amazon_choice(self, asinresult, asin):
        status = True
        try:
            asinresult.find_element_by_id("AMAZONS_CHOICE_"+ asin + "-supplementary")
            print(("**** 产品是AmazonChoice。。。。"), flush=True)
        except NoSuchElementException as msg:
            status = False
        finally:
            return status

    def is_asin_bestseller(self, asinresult, asin):
        status = True
        try:
            asinresult.find_element_by_id("BESTSELLER_" + asin + "-supplementary")
            print(("**** 产品是Best Seller。。。"), flush=True)
        except NoSuchElementException as msg:
            status = False
        finally:
            return status

    def is_asin_sponsored(self, asinresult, asin):
        status =True
        try:
            asinresult.find_element_by_id("a-popover-sponsored-header-" + asin)
        except NoSuchElementException as msg:
            status = False
        finally:
            return status

    def click_asin_by_img_jp_small(self, asinresult, asin):
        asinresult.find_element(*self.locator.ASINIMAGE_JP).click()

    def click_asin_by_title_jp(self, asinresult, asin):
        if self.is_asin_sponsored(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_SP_JP).click()
        else:
            asinresult.find_element(*self.locator.ASINTITLE_JP).click()

    def click_asin_by_img_us(self, asinresult, asin):
        if self.is_asin_amazon_choice(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US_AC).click()
        elif self.is_asin_bestseller(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US_BS).click()
        elif self.is_asin_sponsored(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US).click()
        else:
            asinresult.find_element(*self.locator.ASINIMAGE_US).click()

    def click_asin_by_img_us_small(self, asinresult, asin):
        if self.is_asin_amazon_choice(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US_S).click()
        elif self.is_asin_sponsored(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US_S).click()
        elif self.is_asin_bestseller(asinresult, asin):
            asinresult.find_element(*self.locator.ASINIMAGE_US_S).click()
        else:
            asinresult.find_element(*self.locator.ASINIMAGE_US_S).click()

    def click_asin_by_title_us(self, asinresult, asin):
        if self.is_asin_amazon_choice(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_AC).click()
        elif self.is_asin_sponsored(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_SP).click()
        elif self.is_asin_bestseller(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_BS).click()
        else:
            asinresult.find_element(*self.locator.ASINTITLE_US).click()

    def click_asin_by_title_us_small(self, asinresult, asin):
        if self.is_asin_amazon_choice(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_S).click()
        elif self.is_asin_sponsored(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_SP_S).click()
        elif self.is_asin_bestseller(asinresult, asin):
            asinresult.find_element(*self.locator.ASINTITLE_US_S).click()
        else:
            asinresult.find_element(*self.locator.ASINTITLE_US_S).click()

    def enter_asin_page(self, asinresult, asin, begin, end):
        country = self.cf.get("account", "country")
        option = random.randint(1, 2)
        if option == 1:
            print(("**** enter by image link..\n"), flush=True)
            if country == 'us':
                if int(asinresult.size['width']) > 500:
                    self.click_asin_by_img_us(asinresult, asin)
                else:
                    self.click_asin_by_img_us_small(asinresult, asin)
            elif country == "jp":
                self.click_asin_by_img_jp_small(asinresult, asin)
        else:
            print(("**** enter by title link..\n"), flush=True)
            if country == 'us':
                if int(asinresult.size['width']) > 500:
                    self.click_asin_by_title_us(asinresult, asin)
                else:
                    self.click_asin_by_title_us_small(asinresult, asin)
            elif country == "jp":
                self.click_asin_by_title_jp(asinresult, asin)
        print(("*** 进入产品页面 + " + asin), flush=True)
        self.random_sleep(begin, end)
        return self.driver.current_window_handle

    def close_page(self):
        self.driver.close()

    def switch_to_new_page(self, currenthandle):
        handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        for handle in handles:  # 切换窗口（切换到搜狗）
            if handle != currenthandle:
                self.driver.switch_to_window(handle)
                break

        # # 切换到当前最新打开的窗口
        # self.driver.switch_to.window(handles[-1])

    def back_prev_page_by_country(self, prev_handle, begin, end):
        country = self.cf.get("account", "country")
        if country == "jp":
            self.back_prev_page_by_type(prev_handle, "new", begin, end)
        elif country == "us":
            self.back_prev_page_by_type(prev_handle, "current", begin, end)

    def back_prev_page_by_type(self, prev_handle, type, begin, end):
        if type == "new":
            self.switch_to_new_page(prev_handle)
            self.close_page()
            self.driver.switch_to_window(prev_handle)
        elif type == "current":
            self.switch_to_new_page(prev_handle)
            self.navigation_back(begin, end)
            self.driver.switch_to_window(prev_handle)
        print(("*** 返回上一页。。。"), flush=True)
        self.random_sleep(begin, end)


    def enter_next_page(self, begin, end):
        print(("** 翻到下一页。。。"), flush=True)
        self.click(*self.locator.PAGENEXTSTRING)
        self.random_sleep(begin, end)