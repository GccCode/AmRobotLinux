#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonpage import AmazonPage
from locator import AmazonAddressPageLocator
import configparser


class AmazonAddressPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonAddressPageLocator
        self.cf = configparser.ConfigParser()
        self.cf.read("info.txt")

    def locator_state_jp(self, state):
        index = 1
        if state.encode('UTF-8').isalpha():
            for s in self.locator.ADDRESSSTATEOPTIONS_EN:
                if state == s:
                    return index
                index = index + 1
        else:
            for s in self.locator.ADDRESSSTATEOPTIONS_ZH:
                if state == s:
                    return index
                index = index + 1
        return 0

    def add_address(self, addresstype, begin, end):
        self.click(*self.locator.ADDADDRESS)
        self.random_sleep(1000, 2000)
        self.fill_in_form(addresstype, begin, end)

    def fill_in_form(self, addresstype, begin, end):
        country = self.cf.get("account", "country")
        if addresstype == "bill":
            if country == "jp":
                self.fill_in_form_jp("bill", begin, end)
            elif country == "us":
                self.fill_in_form_us("bill", begin, end)
        elif addresstype == "fba":
            if country == "jp":
                self.fill_in_form_jp("fba", begin, end)
            elif country == "us":
                self.fill_in_form_us("fba", begin, end)

    def fill_in_form_jp(self, addresstype, begin, end):
        if addresstype == "bill":
            fullname = self.cf.get("bill_address", "fullname")
            line1 = self.cf.get("bill_address", "addressline1")
            phonenumber = self.cf.get("bill_address", "phone")
            city = self.cf.get("bill_address", "city")
            state = self.cf.get("bill_address", "state")
            postalcode = self.cf.get("bill_address", "postalcode")
        elif addresstype == "fba":
            fullname = self.cf.get("fba_address", "fullname")
            line1 = self.cf.get("fba_address", "addressline1")
            phonenumber = self.cf.get("fba_address", "phone")
            state = self.cf.get("fba_address", "state")
            state_index = self.locator_state_jp(state)
            line2 = self.cf.get("fba_address", "addressline2")
            postalcode1 = self.cf.get("fba_address", "postalcode1")
            postalcode2 = self.cf.get("fba_address", "postalcode2")

        if addresstype == "bill":
            self.select(self.locator.UNITEDSTATEINDEX, *self.locator.COUNTRYSELECT)
            self.random_sleep(1000, 2000)

        self.click(*self.locator.FULLNAME)
        self.random_sleep(1000, 2000)
        self.input(fullname, *self.locator.FULLNAME)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSLINE1)
        self.random_sleep(1000, 2000)
        self.input(line1, *self.locator.ADDRESSLINE1)
        self.random_sleep(1000, 2000)

        if addresstype == "fba":
            self.click(*self.locator.ADDRESSLINE2)
            self.random_sleep(1000, 2000)
            self.input(line2, *self.locator.ADDRESSLINE2)
            self.random_sleep(1000, 2000)

        if addresstype == "bill":
            self.click(*self.locator.ADDRESSCITY)
            self.random_sleep(1000, 2000)
            self.input(city, *self.locator.ADDRESSCITY)
            self.random_sleep(1000, 2000)

            self.click(*self.locator.ADDRESSSTATE)
            self.random_sleep(1000, 2000)
            self.input(state, *self.locator.ADDRESSSTATE)
            self.random_sleep(1000, 2000)

            self.click(*self.locator.ADDRESSPOSTALCODE)
            self.random_sleep(1000, 2000)
            self.input(postalcode, *self.locator.ADDRESSPOSTALCODE)
            self.random_sleep(1000, 2000)
        elif addresstype == "fba":
            self.click(*self.locator.ADDRESSPOSTALCODEONE)
            self.random_sleep(1000, 2000)
            self.input(postalcode1, *self.locator.ADDRESSPOSTALCODEONE)
            self.random_sleep(1000, 2000)

            self.click(*self.locator.ADDRESSPOSTALCODETWO)
            self.random_sleep(1000, 2000)
            self.input(postalcode2, *self.locator.ADDRESSPOSTALCODETWO)
            self.random_sleep(1000, 2000)

            self.select(state_index, *self.locator.ADDRESSSTATESELECT)
            self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSPHONE)
        self.random_sleep(1000, 2000)
        self.input(phonenumber, *self.locator.ADDRESSPHONE)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDADDRESSSUBMIT)
        self.random_sleep(begin, end)
        self.wait_page_loaded(*self.locator.ADDADDRESS)

    def fill_in_form_us(self, addresstype, begin, end):
        if addresstype == "bill":
            fullname = self.cf.get("bill_address", "fullname")
            line1 = self.cf.get("bill_address", "addressline1")
            phonenumber = self.cf.get("bill_address", "phone")
            city = self.cf.get("bill_address", "city")
            state = self.cf.get("bill_address", "state")
            postalcode = self.cf.get("bill_address", "postalcode")
        elif addresstype == "fba":
            fullname = self.cf.get("fba_address", "fullname")
            line1 = self.cf.get("fba_address", "addressline1")
            phonenumber = self.cf.get("fba_address", "phone")
            city = self.cf.get("fba_address", "city")
            state = self.cf.get("fba_address", "state")
            postalcode = self.cf.get("fba_address", "postalcode")

        self.click(*self.locator.FULLNAME)
        self.random_sleep(1000, 2000)
        self.input(fullname, *self.locator.FULLNAME)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSLINE1)
        self.random_sleep(1000, 2000)
        self.input(line1, *self.locator.ADDRESSLINE1)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSCITY)
        self.random_sleep(1000, 2000)
        self.input(city, *self.locator.ADDRESSCITY)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSSTATE)
        self.random_sleep(1000, 2000)
        self.input(state, *self.locator.ADDRESSSTATE)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSPOSTALCODE)
        self.random_sleep(1000, 2000)
        self.input(postalcode, *self.locator.ADDRESSPOSTALCODE)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDRESSPHONE)
        self.random_sleep(1000, 2000)
        self.input(phonenumber, *self.locator.ADDRESSPHONE)
        self.random_sleep(1000, 2000)

        self.click(*self.locator.ADDADDRESSSUBMIT)
        self.random_sleep(begin, end)
        self.wait_page_loaded(*self.locator.ADDADDRESS)

    # def fill_in_form(self, addresstype, begin, end):
    #     country = self.cf.get("account", "country")
    #     if addresstype == "bill":
    #         fullname = self.cf.get("bill_address", "fullname")
    #         line1 = self.cf.get("bill_address", "addressline1")
    #         phonenumber = self.cf.get("bill_address", "phone")
    #         if country == "us":
    #             city = self.cf.get("bill_address", "city")
    #             state = self.cf.get("bill_address", "state")
    #             postalcode = self.cf.get("bill_address", "postalcode")
    #         elif country == "jp":
    #             city = self.cf.get("bill_address", "city")
    #             state = self.cf.get("bill_address", "state")
    #             postalcode = self.cf.get("bill_address", "postalcode")
    #             # state = self.cf.get("bill_address", "state")
    #             # state_index = self.locator_state_jp(state)
    #             # line2 = self.cf.get("bill_address", "addressline2")
    #             # postalcode1 = self.cf.get("bill_address", "postalcode1")
    #             # postalcode2 = self.cf.get("bill_address", "postalcode2")
    #     elif addresstype == "fba":
    #         fullname = self.cf.get("fba_address", "fullname")
    #         line1 = self.cf.get("fba_address", "addressline1")
    #         phonenumber = self.cf.get("fba_address", "phone")
    #         if country == "us":
    #             city = self.cf.get("fba_address", "city")
    #             state = self.cf.get("fba_address", "state")
    #             postalcode = self.cf.get("fba_address", "postalcode")
    #         elif country == "jp":
    #             state = self.cf.get("fba_address", "state")
    #             state_index = self.locator_state_jp(state)
    #             line2 = self.cf.get("fba_address", "addressline2")
    #             postalcode1 = self.cf.get("fba_address", "postalcode1")
    #             postalcode2 = self.cf.get("fba_address", "postalcode2")
    #
    #     if country == "jp" and addresstype == "bill":
    #         self.select(self.locator.UNITEDSTATEINDEX, *self.locator.COUNTRYSELECT)
    #         self.random_sleep(1000, 2000)
    #
    #     self.click(*self.locator.FULLNAME)
    #     self.random_sleep(1000, 2000)
    #     self.input(fullname, *self.locator.FULLNAME)
    #     self.random_sleep(1000, 2000)
    #
    #     self.click(*self.locator.ADDRESSLINE1)
    #     self.random_sleep(1000, 2000)
    #     self.input(line1, *self.locator.ADDRESSLINE1)
    #     self.random_sleep(1000, 2000)
    #
    #     if country == "jp" and addresstype == "fba":
    #         self.click(*self.locator.ADDRESSLINE2)
    #         self.random_sleep(1000, 2000)
    #         self.input(line2, *self.locator.ADDRESSLINE2)
    #         self.random_sleep(1000, 2000)
    #
    #     if country == "us" or (country == "jp" and addresstype == "bill"):
    #         self.click(*self.locator.ADDRESSCITY)
    #         self.random_sleep(1000, 2000)
    #         self.input(city, *self.locator.ADDRESSCITY)
    #         self.random_sleep(1000, 2000)
    #
    #         self.click(*self.locator.ADDRESSSTATE)
    #         self.random_sleep(1000, 2000)
    #         self.input(state, *self.locator.ADDRESSSTATE)
    #         self.random_sleep(1000, 2000)
    #
    #         self.click(*self.locator.ADDRESSPOSTALCODE)
    #         self.random_sleep(1000, 2000)
    #         self.input(postalcode, *self.locator.ADDRESSPOSTALCODE)
    #         self.random_sleep(1000, 2000)
    #     elif country == "jp" and addresstype == "fba":
    #         self.click(*self.locator.ADDRESSPOSTALCODEONE)
    #         self.random_sleep(1000, 2000)
    #         self.input(postalcode1, *self.locator.ADDRESSPOSTALCODEONE)
    #         self.random_sleep(1000, 2000)
    #
    #         self.click(*self.locator.ADDRESSPOSTALCODETWO)
    #         self.random_sleep(1000, 2000)
    #         self.input(postalcode2, *self.locator.ADDRESSPOSTALCODETWO)
    #         self.random_sleep(1000, 2000)
    #
    #         self.select(state_index, *self.locator.ADDRESSSTATESELECT)
    #         self.random_sleep(1000, 2000)
    #
    #     self.click(*self.locator.ADDRESSPHONE)
    #     self.random_sleep(1000, 2000)
    #     self.input(phonenumber, *self.locator.ADDRESSPHONE)
    #     self.random_sleep(1000, 2000)
    #
    #     self.click(*self.locator.ADDADDRESSSUBMIT)
    #     self.random_sleep(begin, end)
    #     self.wait_page_loaded(*self.locator.ADDADDRESS)


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
#     accountpage.enter_address_page()
#     page.random_sleep(3000, 5000)
#     addresspage = AmazonAddressPage(driver)
#     addresspage.add_address("bill")
#     page.random_sleep(3000, 5000)
#
#     page.enter_account_page()
#     page.random_sleep(3000, 5000)
#     accountpage.enter_address_page()
#     page.random_sleep(3000, 5000)
#     addresspage.add_address("fba")
#     page.random_sleep(3000, 5000)
#     driver.quit()