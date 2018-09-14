#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonpage import AmazonPage
from locator import AmazonRegisterPageLocator
import configparser

class AmazonRegisterPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonRegisterPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")

    def register(self, begin, end):
        self.fill_in_form()
        self.random_sleep(begin, end)

    def fill_in_form(self):
        username = self.cf.get("account", "username")
        country = self.cf.get("account", "country")
        emailname = self.cf.get("account", "email")
        password = self.cf.get("account", "password")
        self.click(*self.locator.USERENAME)
        self.random_sleep(1000, 2000)
        self.input(username, *self.locator.USERENAME)
        self.random_sleep(1000, 3000)
        if country == 'jp':
            pronunciation = self.cf.get("account", "pronunciation")
            self.click(*self.locator.PRONUNCIATION)
            self.random_sleep(1000, 2000)
            self.input(pronunciation, *self.locator.PRONUNCIATION)
        self.click(*self.locator.EMAILNAME)
        self.random_sleep(1000, 2000)
        self.input(emailname, *self.locator.EMAILNAME)
        self.random_sleep(1000, 3000)
        self.click(*self.locator.PASSWORD)
        self.random_sleep(1000, 2000)
        self.input(password, *self.locator.PASSWORD)
        self.random_sleep(1000, 3000)
        self.click(*self.locator.PASSWORDCHECK)
        self.random_sleep(1000, 2000)
        self.input(password, *self.locator.PASSWORDCHECK)
        self.random_sleep(1000, 3000)
        self.click(*self.locator.CONTINUESUBMIT)
#
# if __name__ == "__main__":
#     option = webdriver.ChromeOptions()
#     option.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile 6")
#     driver = webdriver.Chrome(chrome_options=option)
#     #driver = webdriver.Chrome()
#     driver.set_page_load_timeout(30)
#     driver.set_script_timeout(30)
#     page = AmazonPage(driver)
#     page.enter_amazon_page()
#     page.random_sleep(3000, 5000)
#     page.enter_register_page()
#     page.random_sleep(3000, 5000)
#     registerpage = AmazonRegisterPage(driver)
#     registerpage.fill_in_form()
#     page.random_sleep(3000, 5000)
#     driver.quit()
