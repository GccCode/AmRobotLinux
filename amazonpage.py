#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time as tm
import random
import json
import os
from baseaction import BaseAction
from locator import AmazonPageLocator
import pyautogui
import configparser
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


class AmazonPage(BaseAction):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")
        self.screen_width = pyautogui.size()[0]
        self.screen_heigth = pyautogui.size()[1]

    def get_cookies(self):
        return self.driver.get_cookies()

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        if os.path.exists('cookies.json'):
            os.remove('cookies.json')
        with open('cookies.json', 'w') as f:
            f.write(jsonCookies)

    def load_cookies(self):
        if os.path.exists('cookies.json'):
            with open('cookies.json', 'r', encoding='utf-8') as f:
                listCookies = json.loads(f.read())
            for cookie in listCookies:
                if 'expiry' in cookie:
                    self.driver.add_cookie({
                        'domain': cookie['domain'],
                        'expiry': str(cookie['expiry']),
                        'name': cookie['name'],
                        'path': cookie['path'],
                        'value': cookie['value']
                    })
                else:
                    self.driver.add_cookie({
                        'domain': cookie['domain'],
                        'name': cookie['name'],
                        'path': cookie['path'],
                        'value': cookie['value']
                    })

    def enter_amazon_page(self, begin, end):
        try:
            country = self.cf.get("account", "country")
            if country == 'us':
                self.driver.get('https://www.amazon.com')
            elif country == 'jp':
                self.driver.get('https://www.amazon.co.jp')
            elif country == 'ca':
                self.driver.get('https://www.amazon.ca')
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        self.random_sleep(begin, end)
        if os.path.exists('cookies.json'):
            print(("** 加载cookies。。。。"), flush=True)
            self.load_cookies()
            self.random_sleep(2000, 3000)

    def get_currenthandle(self):
        return self.driver.current_window_handle

    def enter_super_link(self, link, begin, end):
        self.driver.get(link)
        self.random_sleep(begin, end)

    def wait_page_loaded(self, *locator):
        self.driver.find_element(*locator)

    def goto_top(self, begin, end):
        self.scoll_to_top()
        self.wait_page_loaded(*self.locator.LOGO)
        self.random_sleep(begin, end)

    def enter_account_page(self, begin, end):
        self.click(*self.locator.ACCOUNT)
        self.random_sleep(begin, end)

    def enter_wishlist(self):
        self.hover(*self.locator.ACCOUNT)
        self.random_sleep(1000, 2000)
        self.click(*self.locator.WISHLIST)

    def enter_cart(self):
        self.click(*self.locator.CART)

    def enter_orders(self):
        self.click(*self.locator.ORDERS)

    def register_prime(self, begin, end):
        self.click(*self.locator.PRIME)
        self.random_sleep(1000, 2000)
        self.click(*self.locator.PRIMEFREETRIAL)
        self.random_sleep(1000, 2000)
        self.click(*self.locator.PRIMESTARTTRIAL)

        self.random_sleep(begin, end)

    def navigation_back(self, begin, end):
        self.driver.back()
        self.random_sleep(begin, end)

    def random_walk(self, count):
        t1 = tm.time()
        i = 0
        while i < count:
            self.random_mouse_move()
            self.random_mouse_scoll()
            i += 1

        t2 = tm.time()
        print(("**** random walk次数：" + str(count) + " + 总耗时： " + format(t2 - t1)), flush=True)

    def enter_signin_page(self, begin, end):
        self.hover(*self.locator.ACCOUNT)
        self.random_sleep(1000, 2000)

        try:
            self.click(*self.locator.SIGNOUT)
        except NoSuchElementException as msg:
            self.click(*self.locator.SIGNIN)

        self.random_sleep(begin, end)

    def enter_register_page(self, begin, end):
        result = random.randint(1,2)
        if result == 1:
            self.hover(*self.locator.ACCOUNT)
            self.random_sleep(1000, 2000)
            result = random.randint(1, 2)
            if result == 1:
                self.click(*self.locator.SIGNIN)
                self.random_sleep(1000, 2000)
                self.click(*self.locator.CREATEACCOUNTSUBMIT)
            else:
                self.click(*self.locator.STARTHERE)
        else:
            self.click(*self.locator.ACCOUNT)
            self.random_sleep(1000, 2000)
            self.click(*self.locator.CREATEACCOUNTSUBMIT)

        self.random_sleep(begin, end)

    def search_asin(self, keyword, begin, end):
        self.input(keyword, *self.locator.SEARCH)
        self.click(*self.locator.SUBMITKEYWORD)

    def wait_searchbox_exsist(self):
        self.wait_element_match(60, True, *self.locator.SEARCH)

# if __name__ == "__main__":
#     #option = webdriver.ChromeOptions()
#     #option.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile 6")
#     #driver = webdriver.Chrome(chrome_options=option)
#     driver = webdriver.Chrome()
#     driver.set_page_load_timeout(30)
#     driver.set_script_timeout(30)
#     page = AmazonPage(driver)
#     page.enter_amazon_page()
#     time.sleep(5)
#     page.search_asin("echo dot")
#     time.sleep(5)
#     page.enter_register_page()
#     driver.quit()