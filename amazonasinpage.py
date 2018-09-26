#!/usr/bin/env python
# -*- coding:utf-8 -*-


import random
from amazonpage import AmazonPage
from locator import AmazonAsinPageLocator
import configparser
from selenium.common.exceptions import NoSuchElementException

class AmazonAsinPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonAsinPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")

    def add_cart(self, begin, end):
        status = True
        try:
            if self.is_element_exsist(*self.locator.ADDCARTBUTTON):
                self.click(*self.locator.ADDCARTBUTTON)
                self.random_sleep(begin, end)
                print(("**** Add Cart..."), flush=True)
            else:
                status = False
                print("Addcart element can't find..", flush=True)
        except:
            print("Addcart element error..", flush=True)
            status = False
        finally:
            return status

    def select_size(self, asin, begin, end):
        if self.is_element_exsist(*self.locator.SELECT_SIZE_JP):
            # element = self.driver.find_element(*self.locator.SELECT_SIZE_JP)
            OPTIONS_JP_PREFIX = 'native_size_name_'
            option_array = []
            total = 0
            for total in range(0, 20):
                try:
                    element = self.driver.find_element_by_id(OPTIONS_JP_PREFIX + str(total))
                    option_array.append(element)
                    print(element.get_attribute('class'))
                    print(element.get_attribute('value'))
                except NoSuchElementException as msg:
                    print("yyyy", flush=True)
                    break
            print(total)

            for index in range(0, total):
                value = option_array[index].get_attribute('value')
                print(asin)
                print(value)
                if asin in value:
                    print(option_array[index].get_attribute('class'))
                    if option_array[index].get_attribute('class') == 'dropdownAvailable':
                        print("sjdflsdjlk")
            input("xxxx")
            # self.select(index, *self.locator.SELECT_SIZE_JP)
            self.random_sleep(begin, end)
        else:
            print("Size Selection is not here", flush=True)

    def ask_qa(self, content, begin, end):
        country = self.cf.get("account", "country")
        self.click(*self.locator.QATEXT)
        self.random_sleep(1000, 2000)
        self.input(content, *self.locator.QATEXT)
        self.random_sleep(3000, 6000)
        if country == "us":
            self.click(*self.locator.QAENTRYBUTTON_US)
        elif country == "jp":
            self.click(*self.locator.QAENTRYBUTTON_JP)
        self.random_sleep(2000, 3000)
        if self.is_element_exsist(*self.locator.QAPOSTBUTTON):
            print(("**** QA post button is ready!"), flush=True)
            self.click(*self.locator.QAPOSTBUTTON)
        self.random_sleep(begin, end)
        print(("**** 提交QA： " + content), flush=True)

    def add_wishlist(self, begin, end, asin):
        country = self.cf.get("account", "country")
        self.click(*self.locator.ADDWISHLISTSUBMITBUTTON)
        self.random_sleep(5000, 8000)
        if self.is_element_exsist(*self.locator.WISHLISTCONTINUE) == True:
            self.window_capture("wishlist" + "-" + asin)
            self.click(*self.locator.WISHLISTCONTINUE)
        else:
            if self.is_element_exsist(*self.locator.CREATELISTBUTTON):
                if country == "us":
                    self.click(*self.locator.WISHLISTSELETE)
                    self.random_sleep(1000, 2000)
                self.click(*self.locator.CREATELISTBUTTON)
                self.random_sleep(3000, 5000)
                if asin != False:
                    self.window_capture("wishlist" + "-" + asin)
                if self.is_element_exsist(*self.locator.WISHLISTCONTINUE1) == True:
                    self.click(*self.locator.WISHLISTCONTINUE1)
                else:
                    print(("**** 新建wishlist找不到返回按钮。。。。"), flush=True)

        print(("**** 添加心愿卡。。。。"), flush=True)
        self.random_sleep(begin, end)

    def review_all(self, begin, end):
         self.click(*self.locator.REVIEWALL)
         self.random_sleep(1000, 2000)
         self.random_walk(random.randint(5, 10))
         print(("**** 浏览评论。。。。"), flush=True)

