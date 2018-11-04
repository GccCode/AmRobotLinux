#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import re
import time
import json
import sys
import io
from selenium.webdriver.common.by import By
from amazonasinpage import AmazonAsinPage
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from amazonpage import AmazonPage
import copy
from datetime import date
from datetime import datetime
from datetime import timedelta
from amazondata import AmazonData
import amazonwrapper
import utils
import traceback
import xlrd
import amazonglobal


LOGO = (By.ID, 'nav-logo')
INEXSISTED_FLAG_JP = (By.CSS_SELECTOR, 'img[alt=\'Amazon\']')
INEXSISTED_FLAG_US = (By.CSS_SELECTOR, 'img[alt=\'Dogs of Amazon\']')
UNKNOWN_NODE_US = (By.XPATH, '//*[@id=\'zg-center-div\']/h4')

BUYER_COUNT = (By.XPATH, '//*[@id=\'olp_feature_div\']/div/span[position()=1]/a')
QA_COUNT = (By.XPATH, '//*[@id=\'askATFLink\']/span')
FBA_FLAG = (By.ID, "SSOFpopoverLink")
AB_FLAG_JP = (By.XPATH, '//*[@id=\'merchant-info\']/a[position()=1]')
# AB_FLAG_US = (By.XPATH, '//*[@id=\'merchant-info\']/text()[position()=1]')
AB_FLAG_US = (By.ID, 'merchant-info')
SELLER_NAME_US = (By.XPATH, '//*[@id=\'merchant-info\']/a[position()=1]')
MULTI_SELLERS_DIV_US = (By.XPATH, '//*[@id=\'olpOfferList\']/div/div[position()=1]/div')
SELLER_IS_FBA_FLAG1_US = (By.ID, 'fulfilledByAmazonPopOver2')
SELLER_IS_FBA_FLAG2_US = (By.CSS_SELECTOR, 'div[class=\'olpBadge\']')
SELLER_IS_FBA_FLAG3_US = (By.CSS_SELECTOR, 'div[id=\'a-popover-fbaPopover\']')
PRIME_CHECKBOX_US = (By.CSS_SELECTOR, 'input[name=\'olpCheckbox_primeEligible\']')
NEW_CHECKBOX_US = (By.CSS_SELECTOR, 'input[name=\'olpCheckbox_new\']')
NEW_US = (By.CSS_SELECTOR, 'span[id=\'olpNew\']')
USED_US = (By.CSS_SELECTOR, 'span[id=\'olpUsed\']')
LIKE_NEW_US = (By.CSS_SELECTOR, 'span[id=\'offerSubCondition\']')
SELLER_NAME_DIV_US = (By.XPATH, './/div[position()=4]/h3[position()=1]/span/a')
SIZE_WEIGHT_TD_US = (By.CSS_SELECTOR, 'td[class=\'a-size-base\']')
NO_THANKS = (By.ID, 'attachSiNoCoverage')
VIEW_CART_BUTTON = (By.ID, 'attach-sidesheet-view-cart-button')
VIEW_CART_BUTTON1 = (By.ID, 'hlb-view-cart')
VIEW_CART_BUTTON2 = (By.CSS_SELECTOR, 'input[name=\'editCart\']')
VIEW_CART_BUTTON3 = (By.CLASS_NAME, 'hlb-cart-button')
DEAL_SYMBOL = (By.XPATH, '//div[contains(@id, \'deal_status_progress_\')]')
DEAL_STATUS = (By.ID, 'goldboxDealStatus')
ITEM_SELECT_US = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/span[position()=1]/select')
ITEM_INPUT_US = (By.CSS_SELECTOR, 'input[name ^=\'quantity\.\']')
ITEM_SUBMIT_US = (By.CSS_SELECTOR, 'input[name ^=\'submit.update-quantity\.\']')
INVENTORY_TIPS_US = (By.XPATH, '//*[@id=\'cart-important-message-box\']/div/div/div/p')
ITEM_DELETE_US = (By.CSS_SELECTOR, 'input[name ^=\'submit.delete\.\']')

PRODUCT_ITEM_JP = (By.XPATH,
                        '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]')
ITEM_INPUT_JP = (By.CSS_SELECTOR, 'input[name ^=\'quantity\.\']')
ITEM_SUBMIT_JP = (By.CSS_SELECTOR, 'input[name ^=\'submit.update-quantity\.\']')
INVENTORY_TIPS_JP = (By.XPATH, '//*[@id=\'cart-important-message-box\']/div/div/div/p')
ITEM_DELETE_JP = (By.CSS_SELECTOR, 'input[name ^=\'submit.delete\.\']')
ITEM_PRICE_JP = (By.ID, 'priceblock_ourprice')
ITEM_OUT_OF_STOCK = (By.ID, 'outOfStock')

CRITICAL_TITLE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_TITLE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/a[position()=1]'

CRITICAL_TITLE_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_TITLE_POSTFIX_US = ']/span/div/span/a[position()=1]'

CRITICAL_FBA_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_FBA_POSTFIX = '2]/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'

CRITICAL_FBA_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_FBA_POSTFIX_US = ']/span/div/span/div[position()=2]/span'

CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'
CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX_US = ']/span/div/span/div[position()=2]/a[position()=1]/span/span'
CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a/span/span'
CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]/span/span'
CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a/span/span'

CRITICAL_REVIEWS_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_REVIEWS_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=2]'
CRITICAL_REVIEWS_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_REVIEWS_POSTFIX_US = ']/span/div/span/div[position()=1]/a[position()=2]'
CRITICAL_RATE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_RATE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]'
CRITICAL_RATE_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_RATE_POSTFIX_US = ']/span/div/span/div[position()=1]/a[position()=1]'
CRITICAL_IMGSRC_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_IMGSRC_POSTFIX = ']/div[position()=1]/div/div[position()=1]/a/img'
CRITICAL_IMGSRC_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_IMGSRC_POSTFIX_US = ']/span/div/span/a[position()=1]/span[position()=1]/div/img'
CRITICAL_RANK_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_RANK_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=1]/span[position()='
CRITICAL_RANK_PREFIX_US = '//*[@id=\'zg-ordered-list\']/li[position()='
CRITICAL_RANK_POSTFIX_US = ']/span/div/div[position()=1]/span[position()=1]/span'

NON_CRITICAL_TITLE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_TITLE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/a[position()=1]'

NON_CRITICAL_FBA_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_FBA_POSTFIX = '2]/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'

NON_CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'
NON_CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a/span/span'
NON_CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]/span/span'
NON_CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a/span/span'

NON_CRITICAL_REVIEWS_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_REVIEWS_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=2]'
NON_CRITICAL_RATE_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_RATE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]'
NON_CRITICAL_IMGSRC_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_IMGSRC_POSTFIX = ']/div[position()=1]/div/div[position()=1]/a/img'
NON_CRITICAL_RANK_PREFIX = '//*[@id=\'zg_nonCritical\']/div[position()='
NON_CRITICAL_RANK_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=1]/span[position()='

class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def getasinfromhref(template):
    rule = r'dp/(.*?)/ref'
    slotList = re.findall(rule, template)
    return slotList[0]

def getimgidfromhref(template):
    rule = r'I/(.*?)\.'
    slotList = re.findall(rule, template)
    if len(slotList[0]) > 20:
        print(template, flush=True)
    return slotList[0]

def getsale_jp(template):
    try:
        rule = r'、(.*?)点'
        slotList = re.findall(rule, template)
        return slotList[0]
    except:
        print(template, flush=True)
        print(traceback.format_exc(), flush=True)

def getsale_us(template):
    rule = r'the (.*?) available'
    slotList = re.findall(rule, template)
    if len(slotList) < 1:
        rule = r'only (.*?) of'
        slotList = re.findall(rule, template)
        if len(slotList) < 1:
            return 0
        else:
            if len(slotList[0]) > 4:
                print(template, flush=True)
                print(slotList[0].split(' ')[len(slotList[0].split(' ')) - 1], flush=True)
                return slotList[0].split(' ')[len(slotList[0].split(' ')) - 1]
            return slotList[0]
    else:
        if len(slotList[0]) > 4:
            print(template, flush=True)
            print(slotList[0].split(' ')[len(slotList[0].split(' ')) - 1], flush=True)
            return slotList[0].split(' ')[len(slotList[0].split(' ')) - 1]
        return slotList[0]

def getseller_jp(template):
    return template.split('：')[1]

def getseller_us(template):
    try:
        rule = r'\((.*?)\)'
        slotList = re.findall(rule, template)
        return slotList[0]
    except:
        return 0

def getqa_jp(template):
    rule = r'(.*?)人'
    slotList = re.findall(rule, template)
    return slotList[0].strip('+')

def getqa_us(template):
    return template.split(' ')[0].strip('+')

def getprice_jp(price):
    if '-' in price:
        return float(price.split('-')[0].strip('￥ ').replace(',', ''))
    else:
        return float(price.strip('￥ ').replace(',', ''))

def getprice_us(price):
    if '-' in price:
        return float(price.split('-')[0].strip('$ ').replace(',', ''))
    else:
        return float(price.strip('$ ').replace(',', ''))

def insert_task_node(table, data):
    amazontask_db_name = amazonglobal.db_name_task
    amazondata = AmazonData()
    status = amazondata.create_database(amazontask_db_name)
    if status == False:
        print("Create Database In Failure + " + amazontask_db_name, flush=True)
    else:
        status = amazondata.connect_database(amazontask_db_name)
        if status == False:
            print("Connect Database In Failure + " + amazontask_db_name, flush=True)
            status = False
        else:
            status = amazondata.create_task_table(table)
            if status != False:
                status = amazondata.insert_task_data(table, data)

            amazondata.disconnect_database()

    return status

class AmazonSpider():
    def __init__(self):
        pass

    def is_all_asin_ok(self, asin_info_array):
        for i in range(len(asin_info_array)):
            tmp_info = asin_info_array[i]
            if tmp_info['status'] == 'no':
                return False
        return True

    def jp_node_gather(self, db_name, node, node_name, type, pages, ips_array, is_sale):
        status = True
        t1 = time.time()
        for page in range(0, pages):
            datetime1 = datetime.strptime('1990-01-28','%Y-%m-%d')
            date1 = datetime1.date()
            asin_info_data = {
                'rank': 0,
                'asin': None,
                'node': node,
                'price': 0,
                'review': 0,
                'rate': 0,
                'qa': 0,
                'shipping': None,
                'seller': 0,
                'avg_sale': 0,
                'inventory_date': date1,
                'limited': 'no',
                'img_url': None,
                'status': 'no'
            }
            asin_info_array = []
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2,
                    # 'javascript': 2
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)
            try:
                amazonpage = AmazonPage(driver)
                url = "https://www.amazon.co.jp/gp/bestsellers/electronics/" + node + "#" + str(page + 1)
                driver.get(url)
                amazonpage.random_sleep(3000, 5000)
                print("Start gathering page: <" + str(page + 1) + "> ##########", flush=True)

                for i in range(0, 3):
                    tmp_symbol = CRITICAL_TITLE_PREFIX + str(i + 1) + CRITICAL_TITLE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['asin'] = getasinfromhref(element.get_attribute('href'))
                        # print("Asin is: " + asin_info_data['asin'], flush=True)

                    tmp_symbol = CRITICAL_REVIEWS_PREFIX + str(i + 1) + CRITICAL_REVIEWS_POSTFIX
                    has_review = amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol))
                    if has_review:
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Review Count is: " + element.text, flush=True)
                        asin_info_data['review'] = int(element.text.strip().replace(',', ''))
                        tmp_symbol = CRITICAL_RATE_PREFIX + str(i + 1) + CRITICAL_RATE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            asin_info_data['rate'] = float(element.get_attribute('title').split(' ')[1])
                            # print("Rate is: " + element.get_attribute('title').split(' ')[1], flush=True)
                    else:
                        asin_info_data['review'] = 0
                        # print("Review Count is: 0", flush=True)
                        asin_info_data['rate'] = 0
                        # print("Rate is: 0", flush=True)
                    if has_review:
                        tmp_symbol = CRITICAL_FBA_PREFIX + str(i + 1) + CRITICAL_FBA_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = 'FBA'
                            # print("FBA", flush=True)
                            tmp_symbol = CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX + str(i + 1) + CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX
                        else:
                            asin_info_data['shipping'] = 'FBM'
                            # print("FBM", flush=True)
                            tmp_symbol = CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX + str(i + 1) + CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_jp(element.text)
                    else:
                        tmp_symbol = CRITICAL_FBA_PREFIX + str(i + 1) + CRITICAL_FBA_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = 'FBA'
                            # print("FBA", flush=True)
                            tmp_symbol = CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX + str(
                                i + 1) + CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX
                        else:
                            asin_info_data['shipping'] = 'FBM'
                            # print("FBM", flush=True)
                            tmp_symbol = CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX + str(
                                i + 1) + CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_jp(element.text)

                    tmp_symbol = CRITICAL_IMGSRC_PREFIX + str(i + 1) + CRITICAL_IMGSRC_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        #  https://images-na.ssl-images-amazon.com/images/I/61EHMhJe1YL._SL500_SR160,160_.jpg
                        asin_info_data['img_url'] = getimgidfromhref(element.get_attribute('src'))
                        # print("ImgSrc is: " + element.get_attribute('src'), flush=True)

                    tmp_symbol = CRITICAL_RANK_PREFIX + str(i + 1) + CRITICAL_RANK_POSTFIX + '2]'
                    if page != 0:
                        tmp_symbol = CRITICAL_RANK_PREFIX + str(i + 1) + CRITICAL_RANK_POSTFIX + '1]'
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Top Rank is: " + element.text.strip().replace('.', ''), flush=True)
                        asin_info_data['rank'] = int(element.text.strip().replace('.', ''))

                        asin_info_array.append(copy.deepcopy(asin_info_data))
                        # print(asin_info_data['asin'], flush=True)
                        # print("** ------------------- **", flush=True)

                for i in range(0, 17):
                    tmp_symbol = NON_CRITICAL_TITLE_PREFIX + str(i + 1) + NON_CRITICAL_TITLE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['asin'] = getasinfromhref(element.get_attribute('href'))
                        # print("Asin is: " + getasinfromhref(element.get_attribute('href')), flush=True)

                    tmp_symbol = NON_CRITICAL_REVIEWS_PREFIX + str(i + 1) + NON_CRITICAL_REVIEWS_POSTFIX
                    has_review = amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol))
                    if has_review:
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Review Count is: " + element.text, flush=True)
                        asin_info_data['review'] = int(element.text.strip().replace(',', ''))
                        tmp_symbol = NON_CRITICAL_RATE_PREFIX + str(i + 1) + NON_CRITICAL_RATE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            asin_info_data['rate'] = float(element.get_attribute('title').split(' ')[1])
                            # print("Rate is: " + element.get_attribute('title').split(' ')[1], flush=True)
                    else:
                        asin_info_data['review'] = 0
                        # print("Review Count is: 0", flush=True)
                        asin_info_data['rate'] = 0
                        # print("Rate is: 0", flush=True)
                    if has_review:
                        tmp_symbol = NON_CRITICAL_FBA_PREFIX + str(i + 1) + NON_CRITICAL_FBA_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = "FBA"
                            # print("FBA", flush=True)
                            tmp_symbol = NON_CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX + str(i + 1) + NON_CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX
                        else:
                            asin_info_data['shipping'] = "FBM"
                            # print("FBM", flush=True)
                            tmp_symbol = NON_CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX + str(i + 1) + NON_CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_jp(element.text)
                    else:
                        tmp_symbol = NON_CRITICAL_FBA_PREFIX + str(i + 1) + NON_CRITICAL_FBA_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = "FBA"
                            # print("FBA", flush=True)
                            tmp_symbol = NON_CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX + str(
                                i + 1) + NON_CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX
                        else:
                            asin_info_data['shipping'] = "FBM"
                            # print("FBM", flush=True)
                            tmp_symbol = NON_CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX + str(
                                i + 1) + NON_CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_jp(element.text)

                    tmp_symbol = NON_CRITICAL_IMGSRC_PREFIX + str(i + 1) + NON_CRITICAL_IMGSRC_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['img_url'] = getimgidfromhref(element.get_attribute('src'))
                        # print("ImgSrc is: " + element.get_attribute('src'), flush=True)


                    tmp_symbol = NON_CRITICAL_RANK_PREFIX + str(i + 1) + NON_CRITICAL_RANK_POSTFIX + '1]'
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Top Rank is: " + element.text.strip().replace('.', ''), flush=True)
                        asin_info_data['rank'] = int(element.text.strip().replace('.', ''))

                        asin_info_array.append(copy.deepcopy(asin_info_data))
                        # print(asin_info_data['asin'], flush=True)
                        # print("** ------------------- **", flush=True)

                amazonpage.random_sleep(2000, 5000)
            except NoSuchElementException as msg:
                status = False
                print("Except: NoSuchElementException", flush=True)
            except Exception as e:
                status = False
                # amazonpage.window_capture('unknown-error')
                print(traceback.format_exc(), flush=True)
                # print(e, flush=True)
            finally:
                driver.quit()
                if status == False:
                    return False

            status = True
            inventory_array = []
            asin_info_remove_array = []
            try:
                while self.is_all_asin_ok(asin_info_array) == False:
                    for i in range(0, len(asin_info_array)):
                        tmp_info = asin_info_array[i]
                        if tmp_info['status'] == 'no':
                            result = self.get_inventory_jp(False, tmp_info['asin'], ips_array, is_sale)
                            if result == False:
                                asin_info_remove_array.append(asin_info_array[i])
                                tmp_info['status'] = 'err'
                            elif result == -111:
                                print("ip problems...", flush=True)
                                tmp_info['status'] = 'no'
                            else:
                                tmp_info['shipping'] = result['shipping']
                                tmp_info['seller'] = result['seller']
                                tmp_info['qa'] = result['qa']
                                tmp_info['limited'] = result['limited']
                                tmp_info['status'] = 'ok'
                                # if result['seller'] == 1:
                                if is_sale:
                                    inventory_array.append(copy.deepcopy(result))
                                # else:
                                #     asin_info_remove_array.append(asin_info_array[i])
            except Exception as e:
                status = False
                # amazonpage.window_capture('unknown-error')
                print(traceback.format_exc(), flush=True)
                # print(str(e), flush=True)
            finally:
                if status == False:
                    return False

            if is_sale:
                for i in range(0, len(asin_info_remove_array)):
                    asin_info_array.remove(asin_info_remove_array[i])
                if len(asin_info_array) != len(inventory_array):
                    print(len(asin_info_array), flush=True)
                    print(len(inventory_array), flush=True)

                amazondata = AmazonData()
                status = amazondata.create_database(db_name)
                if status == True:
                    status = amazondata.connect_database(db_name)
                    if status == True:
                        for i in range(0, len(asin_info_array)):
                            asin = asin_info_array[i]['asin']
                            node_table = node + '_' + type
                            status = amazondata.create_node_table(node_table)
                            if status == True:
                                # print("node_table create sucessfully + " + node_table, flush=True)
                                status = amazondata.insert_node_data(node_table, asin_info_array[i])
                                if status == True:
                                    # print("node_data inserted sucessfully.. + " + node_table, flush=True)
                                    if asin_info_array[i]['limited'] == 'no' and asin_info_array[i]['status'] != 'err' and asin_info_array[i]['shipping'] != 'FBM' and float(asin_info_array[i]['price']) > 800:
                                        inventory_table = 'INVENTORY_' + asin
                                        status = amazondata.create_inventory_table(inventory_table)
                                        if status == True:
                                            # print("inventory_table create sucessfully + " + inventory_table, flush=True)
                                            cur_date = date.today()
                                            data = {
                                                'date' : cur_date,
                                                'inventory' : inventory_array[i]['inventory']
                                            }
                                            status = amazondata.insert_inventory_data(inventory_table, data)
                                            if status == True:
                                                # print("inventory data insert sucessfully.. + " + inventory_table, flush=True)
                                                condition = 'asin=\'' + asin + '\''
                                                value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                                status = amazondata.update_data(node_table, 'inventory_date', value, condition)
                                                if status == True:
                                                    # print("invetory_date update sucessfully.. + " + node_table, flush=True)
                                                    task_data = {
                                                        'node': node,
                                                        'status': 'ok',
                                                        'last_date': cur_date,
                                                        'node_name': node_name
                                                    }
                                                    status = insert_task_node(amazonglobal.table_sale_task_jp, task_data)
                                                    if status == False:
                                                        print("insert task node in failure... + " +  node, flush=True)
                                                    status = amazondata.get_yesterday_sale(inventory_table)
                                                    if status != -999:
                                                        # print("get_yesterday_sale sucessfully.. + " + inventory_table, flush=True)
                                                        yesterday = date.today() + timedelta(days=-1)
                                                        data = {
                                                            'date' : yesterday,
                                                            'sale' : copy.deepcopy(status)
                                                        }
                                                        sale_table = 'SALE_' + asin
                                                        status = amazondata.create_sale_table(sale_table)
                                                        if status == True:
                                                            # print("sale_table create sucessfully.. + " + sale_table, flush=True)
                                                            status = amazondata.insert_sale_data(sale_table, data)
                                                            if status == True:
                                                                # print("sale_data insert sucessfully... + " + sale_table, flush=True)
                                                                avg_sale = amazondata.get_column_avg(sale_table, 'sale')
                                                                if avg_sale != -999:
                                                                    status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                                    if status == False:
                                                                        print("avg_sale update fail.. + " + node_table, flush=True)
                                                                    # else:
                                                                    #     print("avg_sale update successfully.. + " + node_table, flush=True)
                                                                # else:
                                                                #     print(" get avg_sale fail.. + " + node_table, flush=True)
                                                            else:
                                                                print("sale_data insert fail... + " + sale_table, flush=True)
                                                        else:
                                                            print("sale_table create fail.. + " + sale_table, flush=True)
                                                else:
                                                    print("invetory_date update fail.. + " + node_table, flush=True)
                                            else:
                                                print("inventory data insert fail.. + " + inventory_table, flush=True)
                                        else:
                                            print("inventory_table create fail + " + inventory_table, flush=True)
                                    else:
                                        pass
                                        # print('Inventory Limited, no need to record...', flush=True)
                                else:
                                    print("asin_info_data inserted fail.. + " + node_table, flush=True)
                            else:
                                print("node_table create fail + " + node_table, flush=True)

                        amazondata.disconnect_database()
                    else:
                        print("connect_database fail..", flush=True)

        t2 = time.time()
        print("总耗时：" + format(t2 - t1))

        return status

    def us_node_gather(self, db_name, node, node_name, type, pages, ips_array, is_sale):
        status = True
        t1 = time.time()
        for page in range(0, pages):
            datetime1 = datetime.strptime('1990-01-28','%Y-%m-%d')
            date1 = datetime1.date()
            asin_info_data = {
                'rank': 0,
                'asin': None,
                'node': node,
                'price': 0,
                'review': 0,
                'rate': 0,
                'qa': 0,
                'shipping': None,
                'seller': 0,
                'avg_sale': 0,
                'inventory_date': date1,
                'limited': 'no',
                'img_url': None,
                'status': 'no',
                'seller_name': '',
                'size': '',
                'weight': 0
            }
            asin_info_array = []
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2,
                    # 'javascript': 2
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)
            try:
                amazonpage = AmazonPage(driver) # /ref=zg_bs_pg_1?_encoding=UTF8&pg=2
                url = "https://www.amazon.com/gp/bestsellers/electronics/" + node + "/ref=zg_bs_pg_1?_encoding=UTF8&pg=" + str(page + 1)
                driver.get(url)
                amazonpage.random_sleep(3000, 5000)
                print("Start gathering page: <" + str(page + 1) + "> ##########", flush=True)

                for i in range(0, 50):
                    unavailable = False
                    tmp_symbol = CRITICAL_TITLE_PREFIX_US + str(i + 1) + CRITICAL_TITLE_POSTFIX_US
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['asin'] = getasinfromhref(element.get_attribute('href'))
                        # print("Asin is: " + asin_info_data['asin'], flush=True)
                    else:
                        if amazonpage.is_element_exsist(*UNKNOWN_NODE_US) and i == 0:
                            element = driver.find_element(*UNKNOWN_NODE_US)
                            if 'no Best Sellers' in element.text:
                                status = False
                                return status
                        else:
                            continue

                    tmp_symbol = CRITICAL_REVIEWS_PREFIX_US + str(i + 1) + CRITICAL_REVIEWS_POSTFIX_US
                    has_review = amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol))
                    if has_review:
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Review Count is: " + element.text, flush=True)
                        asin_info_data['review'] = int(element.text.strip().replace(',', ''))
                        tmp_symbol = CRITICAL_RATE_PREFIX_US + str(i + 1) + CRITICAL_RATE_POSTFIX_US
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print(element.get_attribute('title'), flush=True)
                            # print(element.get_attribute('title').split(' ')[0], flush=True)
                            asin_info_data['rate'] = float(element.get_attribute('title').split(' ')[0])
                            # print("Rate is: " + element.get_attribute('title').split(' ')[0], flush=True)
                    else:
                        asin_info_data['review'] = 0
                        # print("Review Count is: 0", flush=True)
                        asin_info_data['rate'] = 0
                        # print("Rate is: 0", flush=True)
                    if has_review:
                        tmp_symbol = CRITICAL_FBA_PREFIX_US + str(i + 1) + CRITICAL_FBA_POSTFIX_US
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = 'FBA'
                            # print("FBA", flush=True)
                            tmp_symbol = CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX_US + str(i + 1) + CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX_US
                        else:
                            asin_info_data['shipping'] = 'FBM'
                            # print("FBM", flush=True)
                            tmp_symbol = CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX + str(i + 1) + CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('$ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_us(element.text)
                            if asin_info_data['price'] < 10:
                                continue
                        else:
                            continue
                    else:
                        tmp_symbol = CRITICAL_FBA_PREFIX_US + str(i + 1) + CRITICAL_FBA_POSTFIX_US
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            asin_info_data['shipping'] = 'FBA'
                            # print("FBA", flush=True)
                            tmp_symbol = CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX + str(
                                i + 1) + CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX
                        else:
                            asin_info_data['shipping'] = 'FBM'
                            # print("FBM", flush=True)
                            tmp_symbol = CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX + str(
                                i + 1) + CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX
                        if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                            element = driver.find_element_by_xpath(tmp_symbol)
                            # print("Price is : " + element.text.strip('$ ').replace(',', ''), flush=True)
                            asin_info_data['price'] = getprice_us(element.text)
                            if int(asin_info_data['price']) < 10:
                                continue
                        else:
                            continue

                    tmp_symbol = CRITICAL_IMGSRC_PREFIX_US + str(i + 1) + CRITICAL_IMGSRC_POSTFIX_US
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        #  https://images-na.ssl-images-amazon.com/images/I/61EHMhJe1YL._SL500_SR160,160_.jpg
                        #  https://images-na.ssl-images-amazon.com/images/I/51-29ux0dCL._AC_UL200_SR200,200_.jpg
                        # print("ImgSrc is: " + element.get_attribute('src'), flush=True)
                        asin_info_data['img_url'] = getimgidfromhref(element.get_attribute('src'))

                    tmp_symbol = CRITICAL_RANK_PREFIX_US + str(i + 1) + CRITICAL_RANK_POSTFIX_US
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        # print("Top Rank is: " + element.text.strip().replace('#', ''), flush=True)
                        asin_info_data['rank'] = int(element.text.strip().replace('#', ''))

                        asin_info_array.append(copy.deepcopy(asin_info_data))
                        # print(asin_info_data['asin'], flush=True)
                        # print("** ------------------- **", flush=True)
                    else:
                        continue
                amazonpage.random_sleep(2000, 5000)
            except NoSuchElementException as msg:
                status = False
                print("Except: NoSuchElementException", flush=True)
            except Exception as e:
                status = False
                # amazonpage.window_capture('unknown-error')
                print(traceback.format_exc(), flush=True)
            finally:
                driver.quit()
                if status == False:
                    return False

            status = True
            inventory_array = []
            asin_info_remove_array = []
            amazondata = AmazonData()
            try:
                while self.is_all_asin_ok(asin_info_array) == False:
                    for i in range(0, len(asin_info_array)):
                        tmp_info = asin_info_array[i]
                        if tmp_info['status'] == 'no':
                            result = self.get_inventory_us(False, tmp_info['asin'], ips_array, False, is_sale)
                            if result == False:
                                asin_info_remove_array.append(asin_info_array[i])
                                tmp_info['status'] = 'err'
                            elif result == -111:
                                print("ip problems...", flush=True)
                                tmp_info['status'] = 'no'
                            elif result == -222:
                                print("overweight " + tmp_info['asin'], flush=True)
                                tmp_info['limited'] = 'yes'
                            else:
                                tmp_info['shipping'] = result['shipping']
                                tmp_info['seller'] = result['seller']
                                tmp_info['qa'] = result['qa']
                                tmp_info['limited'] = result['limited']
                                tmp_info['status'] = 'ok'
                                tmp_info['seller_name'] = result['seller_name']
                                tmp_info['size'] = result['size']
                                tmp_info['weight'] = result['weight']


                                if is_sale == True:
                                    inventory_array.append(copy.deepcopy(result))
            except Exception as e:
                status = False
                print(traceback.format_exc(), flush=True)
            finally:
                if status == False:
                    return False

            if is_sale == True:
                for i in range(0, len(asin_info_remove_array)):
                    asin_info_array.remove(asin_info_remove_array[i])

                if len(asin_info_array) != len(inventory_array):
                    print(len(asin_info_array), flush=True)
                    print(len(inventory_array), flush=True)

            status = amazondata.create_database(db_name)
            if status == True:
                status = amazondata.connect_database(db_name)
                if status == True:
                    for i in range(0, len(asin_info_array)):
                        asin = asin_info_array[i]['asin']
                        node_table = node + '_' + type
                        status = amazondata.create_node_table(node_table)
                        if status == True:
                            # print("node_table create sucessfully + " + node_table, flush=True)
                            status = amazondata.insert_node_data(node_table, asin_info_array[i])
                            if status == True:
                                # print("node_data inserted sucessfully.. + " + node_table, flush=True)
                                if asin_info_array[i]['limited'] == 'no' and asin_info_array[i]['status'] != 'err' and asin_info_array[i]['seller'] > 0 and asin_info_array[i]['seller'] < 4 and asin_info_array[i]['price'] >= 10 and is_sale:
                                    inventory_table = 'INVENTORY_' + asin
                                    status = amazondata.create_inventory_table(inventory_table)
                                    if status == True:
                                        # print("inventory_table create sucessfully + " + inventory_table, flush=True)
                                        cur_date = date.today()
                                        data = {
                                            'date' : cur_date,
                                            'inventory' : inventory_array[i]['inventory']
                                        }
                                        status = amazondata.insert_inventory_data(inventory_table, data)
                                        if status == True:
                                            # print("inventory data insert sucessfully.. + " + inventory_table, flush=True)
                                            condition = 'asin=\'' + asin + '\''
                                            value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                            status = amazondata.update_data(node_table, 'inventory_date', value, condition)
                                            if status == True:
                                                # print("invetory_date update sucessfully.. + " + node_table, flush=True)
                                                task_data = {
                                                    'node': node,
                                                    'status': 'ok',
                                                    'last_date': cur_date,
                                                    'node_name': node_name
                                                }
                                                status = insert_task_node(amazonglobal.table_sale_task_us, task_data)
                                                if status == False:
                                                    print("insert task node in failure... + " +  node, flush=True)
                                                status = amazondata.get_yesterday_sale(inventory_table)
                                                if status != -999:
                                                    # print("get_yesterday_sale sucessfully.. + " + inventory_table, flush=True)
                                                    yesterday = date.today() + timedelta(days=-1)
                                                    data = {
                                                        'date' : yesterday,
                                                        'sale' : copy.deepcopy(status)
                                                    }
                                                    sale_table = 'SALE_' + asin
                                                    status = amazondata.create_sale_table(sale_table)
                                                    if status == True:
                                                        # print("sale_table create sucessfully.. + " + sale_table, flush=True)
                                                        status = amazondata.insert_sale_data(sale_table, data)
                                                        if status == True:
                                                            # print("sale_data insert sucessfully... + " + sale_table, flush=True)
                                                            avg_sale = amazondata.get_column_avg(sale_table, 'sale')
                                                            if avg_sale != -999:
                                                                status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                                if status == False:
                                                                    print("avg_sale update fail.. + " + node_table, flush=True)
                                                                # else:
                                                                #     print("avg_sale update successfully.. + " + node_table, flush=True)
                                                            # else:
                                                            #     print(" get avg_sale fail.. + " + node_table, flush=True)
                                                        else:
                                                            print("sale_data insert fail... + " + sale_table, flush=True)
                                                    else:
                                                        print("sale_table create fail.. + " + sale_table, flush=True)
                                            else:
                                                print("invetory_date update fail.. + " + node_table, flush=True)
                                        else:
                                            print("inventory data insert fail.. + " + inventory_table, flush=True)
                                    else:
                                        print("inventory_table create fail + " + inventory_table, flush=True)
                                else:
                                    pass
                                    # print('Inventory Limited, no need to record...', flush=True)
                            else:
                                print("asin_info_data inserted fail.. + " + node_table, flush=True)
                        else:
                            print("node_table create fail + " + node_table, flush=True)

                    amazondata.disconnect_database()
                else:
                    print("connect_database fail..", flush=True)

        t2 = time.time()
        print("总耗时：" + format(t2 - t1))

        return status

    def us_seller_gather(self, db_name, node, node_name, type, filename, ips_array, is_sale):
        status = True
        t1 = time.time()

        datetime1 = datetime.strptime('1990-01-28','%Y-%m-%d')
        date1 = datetime1.date()
        asin_info_data = {
            'rank': 0,
            'asin': None,
            'node': node,
            'price': 0,
            'review': 0,
            'rate': 0,
            'qa': 0,
            'shipping': None,
            'seller': 0,
            'avg_sale': 0,
            'inventory_date': date1,
            'limited': 'no',
            'img_url': 'none',
            'status': 'ok'
        }
        asin_info_array = []
        # chrome_options = webdriver.ChromeOptions()
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2,
        #         # 'javascript': 2
        #     }
        # }
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.set_page_load_timeout(60)
        # driver.set_script_timeout(60)
        try:
            # amazonpage = AmazonPage(driver) # /ref=zg_bs_pg_1?_encoding=UTF8&pg=2

            workbook = xlrd.open_workbook(filename)
            worksheet1 = workbook.sheet_by_index(0)
            num_rows = worksheet1.nrows
            for curr_row in range(1, num_rows):
                row = worksheet1.row_values(curr_row)
                asin_info_data['asin'] = row[1].strip(' ')
                asin_info_data['review'] = int(row[5])
                asin_info_data['rate'] = float(row[6])
                asin_info_data['price'] = float(row[3])
                asin_info_data['rank'] = int(row[0])

                asin_info_array.append(copy.deepcopy(asin_info_data))
                print(asin_info_data, flush=True)
                print("** ------------------- **", flush=True)
        except Exception as e:
            status = False
            print(traceback.format_exc(), flush=True)
        finally:
            if status == False:
                return False

        status = True
        inventory_array = []
        asin_info_remove_array = []
        amazondata = AmazonData()
        try:
            for i in range(0, len(asin_info_array)):
                tmp_info = asin_info_array[i]
                result = self.get_inventory_us(False, tmp_info['asin'], ips_array, False, is_sale)
                if result == False or result == -111:
                    asin_info_remove_array.append(asin_info_array[i])
                    tmp_info['status'] = 'err'
                else:
                    tmp_info['shipping'] = result['shipping']
                    tmp_info['seller'] = result['seller']
                    tmp_info['qa'] = result['qa']
                    tmp_info['limited'] = result['limited']
                    # if result['seller'] == 1:
                    if is_sale == True:
                        inventory_array.append(copy.deepcopy(result))
                    # else:
                    #     asin_info_remove_array.append(asin_info_array[i])

        except Exception as e:
            status = False
            print(traceback.format_exc(), flush=True)
            # print(str(e), flush=True)
        finally:
            if status == False:
                return False

        if is_sale == True:
            for i in range(0, len(asin_info_remove_array)):
                asin_info_array.remove(asin_info_remove_array[i])

            if len(asin_info_array) != len(inventory_array):
                print(len(asin_info_array), flush=True)
                print(len(inventory_array), flush=True)

        status = amazondata.create_database(db_name)
        if status == True:
            status = amazondata.connect_database(db_name)
            if status == True:
                for i in range(0, len(asin_info_array)):
                    asin = asin_info_array[i]['asin']
                    node_table = node + '_' + type
                    status = amazondata.create_node_table(node_table)
                    if status == True:
                        # print("node_table create sucessfully + " + node_table, flush=True)
                        status = amazondata.insert_node_data(node_table, asin_info_array[i])
                        if status == True:
                            # print("node_data inserted sucessfully.. + " + node_table, flush=True)
                            if asin_info_array[i]['limited'] == 'no' and asin_info_array[i]['status'] != 'err' and asin_info_array[i]['seller'] == 1 and is_sale:
                                inventory_table = 'INVENTORY_' + asin
                                status = amazondata.create_inventory_table(inventory_table)
                                if status == True:
                                    # print("inventory_table create sucessfully + " + inventory_table, flush=True)
                                    cur_date = date.today()
                                    data = {
                                        'date' : cur_date,
                                        'inventory' : inventory_array[i]['inventory']
                                    }
                                    status = amazondata.insert_inventory_data(inventory_table, data)
                                    if status == True:
                                        # print("inventory data insert sucessfully.. + " + inventory_table, flush=True)
                                        condition = 'asin=\'' + asin + '\''
                                        value = '\'' + cur_date.strftime("%Y-%m-%d") + '\''
                                        status = amazondata.update_data(node_table, 'inventory_date', value, condition)
                                        if status == True:
                                            # print("invetory_date update sucessfully.. + " + node_table, flush=True)
                                            task_data = {
                                                'node': node,
                                                'status': 'ok',
                                                'last_date': cur_date,
                                                'node_name': node_name
                                            }
                                            status = insert_task_node('sale_task_us', task_data)
                                            if status == False:
                                                print("insert task node in failure... + " +  node, flush=True)
                                            status = amazondata.get_yesterday_sale(inventory_table)
                                            if status != -999:
                                                # print("get_yesterday_sale sucessfully.. + " + inventory_table, flush=True)
                                                yesterday = date.today() + timedelta(days=-1)
                                                data = {
                                                    'date' : yesterday,
                                                    'sale' : copy.deepcopy(status)
                                                }
                                                sale_table = 'SALE_' + asin
                                                status = amazondata.create_sale_table(sale_table)
                                                if status == True:
                                                    # print("sale_table create sucessfully.. + " + sale_table, flush=True)
                                                    status = amazondata.insert_sale_data(sale_table, data)
                                                    if status == True:
                                                        # print("sale_data insert sucessfully... + " + sale_table, flush=True)
                                                        avg_sale = amazondata.get_column_avg(sale_table, 'sale')
                                                        if avg_sale != -999:
                                                            status = amazondata.update_data(node_table, 'avg_sale', avg_sale, condition)
                                                            if status == False:
                                                                print("avg_sale update fail.. + " + node_table, flush=True)
                                                            # else:
                                                            #     print("avg_sale update successfully.. + " + node_table, flush=True)
                                                        # else:
                                                        #     print(" get avg_sale fail.. + " + node_table, flush=True)
                                                    else:
                                                        print("sale_data insert fail... + " + sale_table, flush=True)
                                                else:
                                                    print("sale_table create fail.. + " + sale_table, flush=True)
                                        else:
                                            print("invetory_date update fail.. + " + node_table, flush=True)
                                    else:
                                        print("inventory data insert fail.. + " + inventory_table, flush=True)
                                else:
                                    print("inventory_table create fail + " + inventory_table, flush=True)
                            else:
                                pass
                                # print('Inventory Limited, no need to record...', flush=True)
                        else:
                            print("asin_info_data inserted fail.. + " + node_table, flush=True)
                    else:
                        print("node_table create fail + " + node_table, flush=True)

                amazondata.disconnect_database()
            else:
                print("connect_database fail..", flush=True)

        t2 = time.time()
        print("总耗时：" + format(t2 - t1))

        return status

    def get_inventory_us(self, driver_upper, asin, ips_array, seller_name, is_sale):
        if driver_upper == False:
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2,
                    'javascript': 2
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            user_prefix = 'lum-customer-hl_ecee3b35-zone-shared_test_api-ip-'
            ip = amazonwrapper.get_ramdon_accessible_ip(ips_array)
            if ip == False:
                print("can't get accessible ip", flush=True)
                exit(-1)
            proxyauth_plugin_path = utils.create_proxyauth_extension(
                proxy_host='zproxy.lum-superproxy.io',
                proxy_port=22225,
                proxy_username=user_prefix+ip,
                proxy_password='o9dagiaeighm'
            )
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_extension(proxyauth_plugin_path)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)
        else:
            driver = driver_upper
        status = False
        data = {
            'shipping'  : 'FBM',
            'seller'    : 0,
            'seller_name': '',
            'size': '',
            'weight': 0,
            'qa'        : 0,
            'inventory' : 0,
            'limited'   : 'no'
        }
        try:
            url = 'https://www.amazon.com/dp/' + asin
            driver.get(url)
            amazonasinpage = AmazonAsinPage(driver)

            amazonasinpage.random_sleep(3000, 5000)

            if amazonasinpage.is_element_exsist(*INEXSISTED_FLAG_US):
                print("ASIN is unaccessible...", flush=True)
                return False

            if driver.title == "Amazon CAPTCHA" or amazonasinpage.is_element_exsist(*LOGO) == False:
                amazonwrapper.mark_unaccessible_ip('us', ip)
                status = -111
                return -111

            amazonasinpage.select_size(asin, 1000, 2000)

            if amazonasinpage.is_element_exsist(*FBA_FLAG):
                data['shipping'] = 'FBA'
            elif amazonasinpage.is_element_exsist(*AB_FLAG_US):
                element = driver.find_element(*AB_FLAG_US)
                # print(element.text, flush=True)
                if 'Ships from and sold by Amazon.com' in element.text:
                    # print("sold by Amazon Basic..", flush=True)
                    data['shipping'] = 'AB'
            else:
                data['shipping'] = 'FBM'

            if amazonasinpage.is_element_exsist(*QA_COUNT):
                element = driver.find_element(*QA_COUNT)
                data['qa'] = int(getqa_us(element.text))
                # print("qa is:")
                # print(getqa_us(element.text), flush=True)
            else:
                data['qa'] = 0

            overweight_flag = False
            size_weight_td_array = driver.find_elements(*SIZE_WEIGHT_TD_US)
            for td_element in size_weight_td_array:
                if ' inches'in td_element.text and 'x' in td_element.text:
                    size_set = td_element.text.strip().split(' inches')[0].replace(' ', '').split('x')
                    if len(size_set) != 3:
                        print("get size err", flush=True)
                        continue
                    length = float(size_set[0].replace(',', '')) * 2.54
                    if length > 30:
                        overweight_flag = True
                        # print("length over " + str(length), flush=True)
                    width = float(size_set[1].replace(',', '')) * 2.54
                    if width > 20:
                        overweight_flag = True
                        # print("width over " + str(width), flush=True)
                    height = float(size_set[1].replace(',', '')) * 2.54
                    if height > 20:
                        overweight_flag = True
                        # print("height over " + str(height), flush=True)
                    size = str(int(length)) + 'x' + str(int(width)) + 'x' + str(int(height))
                    data['size'] = size
                    # print(size, flush=True)
                elif 'ounces' in td_element.text and ' (' not in td_element.text:
                    weight = '%.3f' % (float(td_element.text.strip().replace(',', '').split(' ')[0]) * 28.3495231 / 1000)
                    data['weight'] = weight
                    # print(weight, flush=True)
                elif 'pounds' in td_element.text and ' (' not in td_element.text:
                    weight = '%.3f' % (float(td_element.text.strip().split(' ')[0]) * 28.3495231 / 1000)
                    data['weight'] = weight
                    # print(weight, flush=True)

            if amazonasinpage.is_element_exsist(*BUYER_COUNT):
                element = driver.find_element(*BUYER_COUNT)
                data['seller'] = int(getseller_us(element.text))

                # print("seller is: " + str(data['seller']))
                # print(element.text, flush=True)
            else:
                print("get seller count in failure..", flush=True)
                if overweight_flag == False:
                    status = False
                else:
                    status = -222
                return status

            if amazonasinpage.is_element_exsist(*SELLER_NAME_US):
                element = driver.find_element(*SELLER_NAME_US)
                data['seller_name'] = element.text.strip().replace('\'', '')
            elif data['shipping'] == 'AB':
                data['seller_name'] = 'Amazon'
            else:
                if overweight_flag == False:
                    status = False
                else:
                    status = -222
                return status

            if is_sale and overweight_flag == False:
                if seller_name == False or data['seller_name'] == 'Amazon' or seller_name == 'Amazon':
                    status = amazonasinpage.add_cart(5000, 8000)
                    print("get_inventory_us + " + asin, flush=True)
                else:
                    print("get_inventory_us from multi seller + " + asin, flush=True)
                    amazonasinpage.click(*BUYER_COUNT)
                    amazonasinpage.random_sleep(1000, 2000)
                    prime_checkbox_flag = False
                    if amazonasinpage.is_element_exsist(*PRIME_CHECKBOX_US) and driver.find_element(*PRIME_CHECKBOX_US).is_selected() == False:
                        amazonasinpage.click(*PRIME_CHECKBOX_US)
                        prime_checkbox_flag = True
                        amazonasinpage.random_sleep(1000, 2000)
                        # print("select the prime checkbox", flush=True)

                    if amazonasinpage.is_element_exsist(*NEW_CHECKBOX_US) and driver.find_element(*NEW_CHECKBOX_US).is_selected() == False:
                        amazonasinpage.click(*NEW_CHECKBOX_US)
                        amazonasinpage.random_sleep(1000, 2000)

                    maindiv_element_array = driver.find_elements(*MULTI_SELLERS_DIV_US)
                    index = 0
                    for maindiv_element in maindiv_element_array:
                        index += 1
                        ADDCART_BUTTON_FROM_SELLER = (By.CSS_SELECTOR, 'input[name=\'submit.addToCart\']')
                        if (index - 1) == 0:
                            continue
                        else:
                            fba_flag = False
                            if amazonasinpage.is_element_exsist(*SELLER_IS_FBA_FLAG1_US) or amazonasinpage.is_element_exsist(*SELLER_IS_FBA_FLAG3_US): # or amazonasinpage.is_element_exsist(*SELLER_IS_FBA_FLAG2_US) or amazonasinpage.is_element_exsist(*SELLER_IS_FBA_FLAG3_US):
                                fba_flag = True
                            if (fba_flag and prime_checkbox_flag == False) or prime_checkbox_flag:
                                if amazonasinpage.is_element_exsist_from_parent(maindiv_element, *SELLER_NAME_DIV_US):
                                    seller_name_element = maindiv_element.find_element(*SELLER_NAME_DIV_US)
                                    if amazonasinpage.is_element_exsist_from_parent(maindiv_element, *USED_US):
                                        print("used_us?", flush=True)
                                        continue
                                    if amazonasinpage.is_element_exsist_from_parent(maindiv_element, *LIKE_NEW_US):
                                        element = driver.find_element(*LIKE_NEW_US)
                                        if 'like' in element.text:
                                            print(element.text.strip(), flush=True)
                                            continue
                                    if seller_name in seller_name_element.text:
                                        # print(seller_name, flush=True)
                                        # print(seller_name_element.text, flush=True)
                                        if amazonasinpage.is_element_exsist_from_parent(maindiv_element, *NEW_US) == False:
                                            print("why??????", flush=True)
                                        if amazonasinpage.is_element_exsist_from_parent(maindiv_element, *ADDCART_BUTTON_FROM_SELLER):
                                            amazonasinpage.click(*ADDCART_BUTTON_FROM_SELLER)
                                            # print("click addcart from seller..", flush=True)
                                            amazonasinpage.random_sleep(1000, 2000)
                                            status = True
                                            break
                                        else:
                                            print("can't find the addart button in sellers page..", flush=True)
                                            status = False
                                else:
                                    # print("can't get the seller name..", flush=True)
                                    status = False
                if status == True:
                    if amazonasinpage.is_element_exsist(*NO_THANKS) == True:
                        amazonasinpage.click(*NO_THANKS)

                    amazonasinpage.random_sleep(1000, 2000)
                    if amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON):
                        amazonasinpage.click(*VIEW_CART_BUTTON)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON1):
                        amazonasinpage.click(*VIEW_CART_BUTTON1)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON2):
                        amazonasinpage.click(*VIEW_CART_BUTTON2)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON3):
                        amazonasinpage.click(*VIEW_CART_BUTTON3)
                        amazonasinpage.random_sleep(3000, 5000)
                    else:
                        if amazonasinpage.is_element_exsist(*DEAL_SYMBOL) or amazonasinpage.is_element_exsist(*DEAL_STATUS):
                            print("Listing running deal... + " + asin, flush=True)
                            # status = -2 # deal
                            data['inventory'] = 0
                            status = data
                            amazonasinpage.window_capture(asin + '-dealing-')
                        else:
                            status = False
                            print("View Cart can't be found... + " + asin, flush=True)
                            amazonasinpage.window_capture(asin + '-noviewcart-')

                    if status == True:
                        if amazonasinpage.is_element_exsist(*ITEM_INPUT_US) == False:
                            print("Inventory Input can't be found... + " + asin, flush=True)
                            status = False
                        else:
                            amazonasinpage.input("999", *ITEM_INPUT_US)
                            if amazonasinpage.is_element_exsist(*ITEM_SUBMIT_US) == False:
                                print("Inventory Update can't be found... + " + asin, flush=True)
                                status = False
                            else:
                                amazonasinpage.click(*ITEM_SUBMIT_US)
                                amazonasinpage.random_sleep(3000, 5000)
                                if amazonasinpage.is_element_exsist(*INVENTORY_TIPS_US) == False:
                                    if amazonasinpage.is_element_exsist(*ITEM_INPUT_US):
                                        element = driver.find_element(*ITEM_INPUT_US)
                                        # print("Inventory Over " + element.get_attribute('value') + ' + ' + asin, flush=True)
                                        data['inventory'] = int(element.get_attribute('value'))
                                    else:
                                        print("Inventory Tips can't be found... + " + asin, flush=True)
                                        status = False
                                else:
                                    element = driver.find_element(*INVENTORY_TIPS_US)
                                    if 'a limit' in element.text:
                                        # print("check limited", flush= True)
                                        data['limited'] = 'yes'
                                        data['inventory'] = 0
                                    else:
                                        # ss
                                        # print(getsale_us(element.text), flush=True)
                                        data['inventory'] = int(getsale_us(element.text))
                                        # print("inventory is: " + str(data['inventory']), flush=True)

                                        inventory_table = 'INVENTORY_' + asin
                                        yesterday_inventory = amazonwrapper.get_yesterday_inventory(amazonglobal.db_name_data_us, inventory_table)
                                        if (yesterday_inventory / data['inventory']) > 10:
                                            input("waiting")

                        if amazonasinpage.is_element_exsist(*ITEM_DELETE_US) == False:
                            print("Inventory Delete can't be found... + " + asin, flush=True)
                            status = False
                        else:
                            amazonasinpage.click(*ITEM_DELETE_US)
                            amazonasinpage.random_sleep(2000, 3000)

                    if status != False:
                        # print(data, flush=True)
                        status = data
                else:
                    if amazonasinpage.is_element_exsist(*ITEM_OUT_OF_STOCK) and data['seller'] != None and data['qa'] != None:
                        print("no inventroy.. + " + asin, flush=True)
                        data['inventory'] = 0
                        status = data
                        amazonasinpage.window_capture(asin + '-noinv-')
                    elif amazonasinpage.is_element_exsist(*DEAL_SYMBOL) or amazonasinpage.is_element_exsist(*DEAL_STATUS):
                            print("Listing running deal... + " + asin, flush=True)
                            # status = -2 # deal
                            data['inventory'] = 0
                            status = data
                            amazonasinpage.window_capture(asin + '-dealing-')
                    else:
                        print("no buycart.. + " + asin, flush=True)
                        # amazonasinpage.window_capture(asin + '-nocart-')
            else:
                if overweight_flag:
                    status = -222
                else:
                    status = data
        except NoSuchElementException as msg:
            status = False
            print("Except: NoSuchElementException", flush=True)
        except TimeoutException as msg:
            print("Except: TimeoutException", flush=True)
            amazonwrapper.mark_unaccessible_ip(country, ip)
            status = -111
        except Exception as e:
            status = False
            # amazonasinpage.window_capture(asin + '-unknown-error')
            print(traceback.format_exc(), flush=True)
            # print(e, flush=True)
        finally:
            if driver_upper == False:
                driver.quit()
            return status

    def get_inventory_jp(self, driver_upper, asin, ips_array, is_sale):
        if driver_upper == False:
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2,
                    'javascript': 2
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            # host_port = amazonwrapper.get_ramdon_accessible_ip()
            # print("proxy ip is: " + host_port, flush=True)
            # proxy_socks_argument = '--proxy-server=socks5://' + host_port
            # chrome_options.add_argument(proxy_socks_argument)
            user_prefix = 'lum-customer-hl_ecee3b35-zone-shared_test_api-ip-'
            ip = amazonwrapper.get_ramdon_accessible_ip(ips_array)
            if ip == False:
                print("can't get accessible ip", flush=True)
                exit(-1)
            # else:
            #     print("proxy ip is: " + ip, flush=True)
            proxyauth_plugin_path = utils.create_proxyauth_extension(
                proxy_host='zproxy.lum-superproxy.io',
                proxy_port=22225,
                proxy_username=user_prefix+ip,
                proxy_password='o9dagiaeighm'
            )
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_extension(proxyauth_plugin_path)
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)
        else:
            driver = driver_upper
        status = False
        data = {
            'shipping'  : 'FBM',
            'seller'    : None,
            'qa'        : None,
            'inventory' : None,
            'limited'   : 'no'
        }
        try:
            print("get_inventory_jp + " + asin, flush=True)
            url = 'https://www.amazon.co.jp/dp/' + asin
            driver.get(url)
            amazonasinpage = AmazonAsinPage(driver)

            amazonasinpage.random_sleep(3000, 5000)

            if amazonasinpage.is_element_exsist(*INEXSISTED_FLAG_JP):
                print("ASIN is unaccessible...", flush=True)
                return False

            if driver.title == "Amazon CAPTCHA" or amazonasinpage.is_element_exsist(*LOGO) == False:
                amazonwrapper.mark_unaccessible_ip('jp', ip)
                status = -111
                amazonasinpage.window_capture(asin + '-ip-block')
                return -111

            amazonasinpage.select_size(asin, 1000, 2000)

            if amazonasinpage.is_element_exsist(*FBA_FLAG):
                data['shipping'] = 'FBA'
            elif amazonasinpage.is_element_exsist(*AB_FLAG_JP):
                element = driver.find_element(*AB_FLAG_JP)
                if element.text == 'Amazon.co.jp':
                    # print("sold by Amazon Basic..", flush=True)
                    data['shipping'] = 'AB'
            else:
                data['shipping'] = 'FBM'

            if amazonasinpage.is_element_exsist(*QA_COUNT):
                element = driver.find_element(*QA_COUNT)
                data['qa'] = int(getqa_jp(element.text))
                # print("qa is:")
                # print(getqa(element.text), flush=True)
            else:
                data['qa'] = 0

            if amazonasinpage.is_element_exsist(*BUYER_COUNT):
                element = driver.find_element(*BUYER_COUNT)
                data['seller'] = int(getseller_jp(element.text))

                # print("seller is: " + str(data['seller']))
                # print(element.text, flush=True)
            else:
                data['seller'] = 0

            if is_sale:
                status = amazonasinpage.add_cart(5000, 8000)
                if status == True:
                    if amazonasinpage.is_element_exsist(*NO_THANKS) == True:
                        amazonasinpage.click(*NO_THANKS)

                    amazonasinpage.random_sleep(1000, 2000)
                    if amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON):
                        amazonasinpage.click(*VIEW_CART_BUTTON)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON1):
                        amazonasinpage.click(*VIEW_CART_BUTTON1)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON2):
                        amazonasinpage.click(*VIEW_CART_BUTTON2)
                        amazonasinpage.random_sleep(3000, 5000)
                    elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON3):
                        amazonasinpage.click(*VIEW_CART_BUTTON3)
                        amazonasinpage.random_sleep(3000, 5000)
                    else:
                        if amazonasinpage.is_element_exsist(*DEAL_SYMBOL) or amazonasinpage.is_element_exsist(*DEAL_STATUS):
                            print("Listing running deal... + " + asin, flush=True)
                            # status = -2 # deal
                            data['inventory'] = 0
                            status = data
                            amazonasinpage.window_capture(asin + '-dealing-')
                        else:
                            status = False
                            print("View Cart can't be found... + " + asin, flush=True)
                            amazonasinpage.window_capture(asin + '-noviewcart-')

                    if status == True:
                        if amazonasinpage.is_element_exsist(*ITEM_INPUT_JP) == False:
                            print("Inventory Input can't be found... + " + asin, flush=True)
                            status = False
                        else:
                            amazonasinpage.input("999", *ITEM_INPUT_JP)
                            if amazonasinpage.is_element_exsist(*ITEM_SUBMIT_JP) == False:
                                print("Inventory Update can't be found... + " + asin, flush=True)
                                status = False
                            else:
                                amazonasinpage.click(*ITEM_SUBMIT_JP)
                                amazonasinpage.random_sleep(3000, 5000)
                                if amazonasinpage.is_element_exsist(*INVENTORY_TIPS_JP) == False:
                                    if amazonasinpage.is_element_exsist(*ITEM_INPUT_JP):
                                        element = driver.find_element(*ITEM_INPUT_JP)
                                        # print("Inventory Over " + element.get_attribute('value') + ' + ' + asin, flush=True)
                                        data['inventory'] = int(element.get_attribute('value'))
                                    else:
                                        print("Inventory Tips can't be found... + " + asin, flush=True)
                                        status = False
                                else:
                                    element = driver.find_element(*INVENTORY_TIPS_JP)
                                    # この商品は、273点のご注文に制限させていただいております。詳しくは、商品の詳細ページをご確認ください。
                                    # この出品者が出品している Amazon Echo Dot 壁掛け ハンガー ホルダー エコードット専用 充電ケーブル付き 充電しながら使用可能 エコードット スピーカー スタンド 保護ケース Alexa アレクサ 第2世代専用 壁掛け カバー (白) の購入は、お客様お一人あたり10までと限定されていますので、注文数を Amazon Echo Dot 壁掛け ハンガー ホルダー エコードット専用 充電ケーブル付き 充電しながら使用可能 エコードット スピーカー スタンド 保護ケース Alexa アレクサ 第2世代専用 壁掛け カバー (白) から10に変更しました。
                                    if '客様お一人' in element.text:
                                        # print("check limited", flush= True)
                                        data['limited'] = 'yes'
                                        data['inventory'] = 0
                                    else:
                                        # ss
                                        data['inventory'] = int(getsale_jp(element.text))
                                        # print("inventory is: " + str(data['inventory']), flush=True)
                        if amazonasinpage.is_element_exsist(*ITEM_DELETE_JP) == False:
                            print("Inventory Delete can't be found... + " + asin, flush=True)
                            status = False
                        else:
                            amazonasinpage.click(*ITEM_DELETE_JP)
                            amazonasinpage.random_sleep(2000, 3000)

                    if status != False:
                        # print(data, flush=True)
                        status = data
                else:
                    if amazonasinpage.is_element_exsist(*ITEM_OUT_OF_STOCK) and data['seller'] != None and data['qa'] != None:
                        print("no inventroy.. + " + asin, flush=True)
                        data['inventory'] = 0
                        status = data
                        amazonasinpage.window_capture(asin + '-noinv-')
                    elif amazonasinpage.is_element_exsist(*DEAL_SYMBOL) or amazonasinpage.is_element_exsist(*DEAL_STATUS):
                            print("Listing running deal... + " + asin, flush=True)
                            # status = -2 # deal
                            data['inventory'] = 0
                            status = data
                            amazonasinpage.window_capture(asin + '-dealing-')
                    else:
                        print("no buycart.. + " + asin, flush=True)
                        amazonasinpage.window_capture(asin + '-nocart-')
            else:
                status = data
        except NoSuchElementException as msg:
            status = False
            print("Except: NoSuchElementException", flush=True)
        except TimeoutException as msg:
            print("Except: TimeoutException", flush=True)
            amazonwrapper.mark_unaccessible_ip(country, ip)
            status = -111
        except Exception as e:
            status = False
            # amazonasinpage.window_capture(asin + 'unknown-error')
            print(traceback.format_exc(), flush=True)
            # print(e, flush=True)
        finally:
            if driver_upper == False:
                driver.quit()
            return status

def amspider_from_file(node_file, type, country, is_sale, db_name):
    ips_array = amazonwrapper.get_all_accessible_ip(country)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    amazonspider = AmazonSpider()
    try:
        f = open(node_file)  # 返回一个文件对象
        line = f.readline()  # 调用文件的 readline()方法
        while line:
            t1 = time.time()
            if len(line.strip('\n')) > 0:
                node = line.strip('\n')
                print(node, flush=True)
                node_name = False
                if country == 'us':
                    node_name = amazonwrapper.get_node_name_from_all('node_info_us', node, country)
                elif country == 'jp':
                    node_name = amazonwrapper.get_node_name_from_all('node_info', node, country)

                if node_name == False:
                    print("get node name in failure..", flush=True)
                    exit(-1)
                if country == 'jp':
                    amazonspider.jp_node_gather(db_name, node, node_name, type, 3, ips_array, is_sale)
                elif country == 'us':
                    amazonspider.us_node_gather(db_name, node, node_name, type, 2, ips_array, is_sale)

                t2 = time.time()
                print("Total Time：" + format(t2 - t1), flush=True)
                f_ok = open('ok' + node_file, 'a')
                f_ok.write(line)
                f_ok.close()

            line = f.readline()

        f.close()
    except Exception as e:
        print(str(e), flush=True)

def amspider_from_mysql(db_name, table, condition, type, country, is_sale):
    ips_array = amazonwrapper.get_all_accessible_ip(country)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    amazonspider = AmazonSpider()
    try:
        condition = condition + ' and status<>\'ok\' and status<>\'err\' and status<>\'run\''
        node_info = amazonwrapper.get_one_data(db_name, table, condition)
        while node_info != False:
            t1 = time.time()
            node = node_info[0]
            node_name = node_info[1]
            sql_condition = 'node=' + '\'' + node + '\''
            status = amazonwrapper.update_data(db_name, table, 'status', '\'run\'', sql_condition)
            if status != False:
                if amazonwrapper.is_in_task_delete_data(country, node) == False:
                    if country == 'jp':
                        status = amazonspider.jp_node_gather(amazonglobal.db_name_data_jp, node, node_name, type, 1, ips_array, is_sale)
                    elif country == 'us':
                        status = amazonspider.us_node_gather(amazonglobal.db_name_data_us, node, node_name, type, 2, ips_array, is_sale)
                    if status != False and status != -111:
                        status = amazonwrapper.update_data(db_name, table, 'status', '\'ok\'', sql_condition)
                        if status != False:
                            print("amspider finish " + node, flush=True)
                    elif status == False:
                        status = amazonwrapper.update_data(db_name, table, 'status', '\'err\'', sql_condition)
                    elif status == -111:
                        status = amazonwrapper.update_data(db_name, table, 'status', '\'no\'', sql_condition)

            node_info = amazonwrapper.get_one_data(db_name, table, condition)
            # t2 = time.time()
            # print("Total Time：" + format(t2 - t1), flush=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        amazonwrapper.update_data(db_name, table, 'status', '\'no\'', sql_condition)

def amspider_test(country):
    ips_array = amazonwrapper.get_all_accessible_ip(country)
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    amazonspider = AmazonSpider()
    try:
        status = amazonspider.get_inventory_us(False, 'B005LJQPE0', ips_array, 'BlueRigger', True)
    except Exception as e:
        print(str(e), flush=True)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    amspider_test('us')
    exit()
    node_file = sys.argv[1]
    if node_file != '0':
        type = sys.argv[2]
        country = sys.argv[3]
        if sys.argv[4] == '1':
            is_sale = True
        elif sys.argv[4] == '0':
            is_sale = False
        db_name = sys.argv[5]
        amspider_from_file(node_file, type, country, is_sale, db_name)
    else: # python3.6 amspider.py 0 BS us 1 node_info_us automotive node=\'10350150011\'
        type = sys.argv[2]
        country = sys.argv[3]
        if sys.argv[4] == '1':
            is_sale = True
        elif sys.argv[4] == '0':
            is_sale = False
        db_name = sys.argv[5]
        table = sys.argv[6]
        condition = sys.argv[7]
        # print(condition, flush=True)
        amspider_from_mysql(db_name, table, condition, type, country, is_sale)

