#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonpage import AmazonPage
from locator import AmazonPaymentPageLocator
import configparser


class AmazonPaymentPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonPaymentPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")

    def add_new_payment(self, begin, end):
        fullname = self.cf.get("bill_address", "fullname")
        cardnum = self.cf.get("cardinfo", "cardnumber")
        validmonth = self.cf.get("cardinfo", "month")
        validyear = self.cf.get("cardinfo", "year")
        country = self.cf.get("account", "country")

        if country == "us":
            if self.is_element_exsist(*self.locator.CARDHOLDER_US):
                self.click(*self.locator.CARDHOLDER_US)
                self.random_sleep(1000, 2000)
                self.input(fullname, *self.locator.CARDHOLDER_US)
                self.random_sleep(1000, 2000)
            else:
                print("找不到持卡人输入栏", flush=True)
                exit(0)
            if self.is_element_exsist(*self.locator.CARDNUMBER_US):
                self.click(*self.locator.CARDNUMBER_US)
                self.random_sleep(1000, 2000)
                self.input(cardnum, *self.locator.CARDNUMBER_US)
                self.random_sleep(1000, 2000)
            else:
                print("找不到卡号输入栏", flush=True)
                exit(0)
            if self.is_element_exsist(*self.locator.VALIDMON_US):
                self.select((int(validmonth) - 1), *self.locator.VALIDMON_US)
                self.random_sleep(1000, 2000)
            else:
                print("找不到有效月份下拉框", flush=True)
                exit(0)
            if self.is_element_exsist(*self.locator.VALIDYEAR_US):
                self.select((int(validyear) - 2018), *self.locator.VALIDYEAR_US)
                self.random_sleep(1000, 2000)
            else:
                print("找不到有效年份下拉框", flush=True)
                exit(0)

            if self.is_element_exsist(*self.locator.ADDCARD_US):
                self.click(*self.locator.ADDCARD_US)
                self.random_sleep(2000, 4000)
            else:
                print("找不到添加卡按钮", flush=True)
                exit(0)
            if self.is_element_exsist(*self.locator.USETHISADDRESS_US):
                self.click(*self.locator.USETHISADDRESS_US)
                self.random_sleep(2000, 4000)
            else:
                print("找不到使用当前地址的按钮", flush=True)
                exit(0)
            if self.is_element_exsist(*self.locator.PAYMENTADDFINISHED):
                self.click(*self.locator.PAYMENTADDFINISHED)
            else:
                print("找不到完成添加卡的按钮", flush=True)
                exit(0)
        elif country == "jp":
            self.click(*self.locator.CARDHOLDER_JP)
            self.random_sleep(1000, 2000)
            self.input(fullname, *self.locator.CARDHOLDER_JP)
            self.random_sleep(1000, 2000)

            self.click(*self.locator.CARDNUMBER_JP)
            self.random_sleep(1000, 2000)
            self.input(cardnum, *self.locator.CARDNUMBER_JP)
            self.random_sleep(1000, 2000)

            self.select((int(validmonth) - 1), *self.locator.VALIDMON_JP)
            self.random_sleep(1000, 2000)
            self.select((int(validyear) - 2018), *self.locator.VALIDYEAR_JP)
            self.random_sleep(1000, 2000)

            self.click(*self.locator.ADDCARD_JP)
            self.random_sleep(2000, 4000)
            self.click(*self.locator.USETHISADDRESS_JP)

        self.random_sleep(begin, end)


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
#     page.enter_account_page()
#     page.random_sleep(3000, 5000)
#     accountpage = AmazonAccountPage(driver)
#     accountpage.enter_payment_page()
#     page.random_sleep(3000, 5000)
#     paymentpage = AmazonPaymentPage(driver)
#     paymentpage.add_new_payment()
#     page.random_sleep(3000, 5000)
#     driver.quit()