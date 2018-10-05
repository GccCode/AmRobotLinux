#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonpage import AmazonPage
import configparser
from locator import AmazonAccountPageLocator


class AmazonAccountPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonAccountPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")

    def enter_address_page(self, begin, end):
        country = self.cf.get("account", "country")
        if country == "us":
            if self.is_element_exsist(*self.locator.YOURADDRESS_US):
                self.click(*self.locator.YOURADDRESS_US)
            elif self.is_element_exsist(*self.locator.YOURADDRESS_US_1):
                self.click(*self.locator.YOURADDRESS_US_1)
            else:
                print("找不到进入地址的入口", flush=True)
                exit(-1)
        elif country == "jp":
            self.click(*self.locator.YOURADDRESS_JP)
        self.random_sleep(begin, end)
        self.wait_page_loaded(*self.locator.ADDADDRESS)

    def enter_payment_page(self, begin, end):
        country = self.cf.get("account", "country")
        if country == "us":
            if self.is_element_exsist(*self.locator.PAYMENTOPTIONS_US):
                self.click(*self.locator.PAYMENTOPTIONS_US)
            elif self.is_element_exsist(*self.locator.PAYMENTOPTIONS_US_1):
                self.click(*self.locator.PAYMENTOPTIONS_US_1)
            else:
                print("找不到支付方式的入口", flush=True)
        elif country == "jp":
            self.click(*self.locator.PAYMENTOPTIONS_JP)
        self.random_sleep(begin, end)
        self.wait_page_loaded(*self.locator.WALLETTITLE)