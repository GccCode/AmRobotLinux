#!/usr/bin/env python
# -*- coding:utf-8 -*-

from amazonpage import AmazonPage
from locator import AmazonCartPageLocator


class AmazonCartPage(AmazonPage):
    def __init__(self, driver):
        self.driver = driver
        self.locator = AmazonCartPageLocator

    def delete_asin(self, asin):
        return

    def clear_cart(self, *asin):
        return

    def checkout(self):
        return