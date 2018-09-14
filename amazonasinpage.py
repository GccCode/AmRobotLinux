#!/usr/bin/env python
# -*- coding:utf-8 -*-


from win32api import GetSystemMetrics
import random
from amazonpage import AmazonPage
from locator import AmazonAsinPageLocator
import configparser


class AmazonAsinPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonAsinPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")
        self.screen_width = GetSystemMetrics(0)
        self.screen_heigth = GetSystemMetrics(1)

    def add_cart(self, begin, end):
        self.click(*self.locator.ADDCARTBUTTON)
        self.random_sleep(begin, end)
        print(("**** 加入购物车。。。"), flush=True)

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

    def add_wishlist(self, begin, end, asin = False):
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

