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


LOGO = (By.ID, 'nav-logo')
INEXSISTED_FLAG_JP = (By.CSS_SELECTOR, 'img[alt=\'Amazon\']')
INEXSISTED_FLAG_US = (By.CSS_SELECTOR, 'img[alt=\'Dogs of Amazon\']')

BUYER_COUNT = (By.XPATH, '//*[@id=\'olp_feature_div\']/div/span[position()=1]/a')
QA_COUNT = (By.XPATH, '//*[@id=\'askATFLink\']/span')
FBA_FLAG = (By.ID, "SSOFpopoverLink")
AB_FLAG_JP = (By.XPATH, '//*[@id=\'merchant-info\']/a[position()=1]')
AB_FLAG_US = (By.XPATH, '//*[@id=\'merchant-info\']/text()[position()=1]')
NO_THANKS = (By.ID, 'attachSiNoCoverage')
VIEW_CART_BUTTON = (By.ID, 'attach-sidesheet-view-cart-button')
VIEW_CART_BUTTON1 = (By.ID, 'hlb-view-cart')
VIEW_CART_BUTTON2 = (By.CSS_SELECTOR, 'input[name=editCart]')
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

CRITICAL_FBA_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_FBA_POSTFIX = '2]/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'

CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a[position()=1]/span/span'
CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=3]/a/span/span'
CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]/span/span'
CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a/span/span'

CRITICAL_REVIEWS_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_REVIEWS_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=2]'
CRITICAL_RATE_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_RATE_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=2]/a[position()=1]'
CRITICAL_IMGSRC_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_IMGSRC_POSTFIX = ']/div[position()=1]/div/div[position()=1]/a/img'
CRITICAL_RANK_PREFIX = '//*[@id=\'zg_critical\']/div[position()='
CRITICAL_RANK_POSTFIX = ']/div[position()=1]/div/div[position()=2]/div[position()=1]/span[position()='

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
    rule = r'、(.*?)点'
    slotList = re.findall(rule, template)
    return slotList[0]

def getsale_us(template):
    rule = r'the (.*?) available'
    slotList = re.findall(rule, template)
    return slotList[0]

def getseller_jp(template):
    return template.split('：')[1]

def getseller_us(template):
    rule = r'\((.*?)\)'
    slotList = re.findall(rule, template)
    return slotList[0]

def getqa_jp(template):
    rule = r'(.*?)人'
    slotList = re.findall(rule, template)
    return slotList[0]

def getqa_us(template):
    return template.split(' ')[0]

def getprice(price):
    if '-' in price:
        return int(price.split('-')[0].strip('￥ ').replace(',', ''))
    else:
        return int(price.strip('￥ ').replace(',', ''))

def insert_task_node(table, data):
    amazontask_db_name = 'amazontask'
    amazondata = AmazonData()
    status = amazondata.connect_database(amazontask_db_name)
    if status == False:
        print("Connect Database In Failure + " + amazontask_db_name, flush=True)
        status = False
    else:
        status = amazondata.insert_task_data(table, data)

        amazondata.disconnect_database()

    return status

class AmazonSpider():
    def __init__(self):
        pass

    def jp_node_gather(self, node, node_name, type, pages, ips_array):
        status = True
        t1 = time.time()
        for page in range(0, pages):
            datetime1 = datetime.strptime('1990-01-28','%Y-%m-%d')
            date1 = datetime1.date()
            asin_info_data = {
                'rank': None,
                'asin': None,
                'node': node,
                'price': None,
                'review': None,
                'rate': None,
                'qa': 0,
                'shipping': None,
                'seller': 0,
                'avg_sale': 0,
                'inventory_date': date1,
                'limited': 'no',
                'img_url': None,
                'status': 'ok'
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
                            asin_info_data['price'] = getprice(element.text)
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
                            asin_info_data['price'] = getprice(element.text)

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
                            asin_info_data['price'] = getprice(element.text)
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
                            asin_info_data['price'] = getprice(element.text)

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
                amazonpage.window_capture('unknown-error')
                print(traceback.format_exc(), flush=True)
                print(e, flush=True)
            finally:
                driver.quit()
                if status == False:
                    return False

            status = True
            # chrome_options = webdriver.ChromeOptions()
            # prefs = {
            #     'profile.default_content_setting_values': {
            #         'images': 2,
            #         'javascript': 2
            #     }
            # }
            # chrome_options.add_experimental_option("prefs", prefs)
            # driver = webdriver.Chrome(chrome_options=chrome_options)
            # driver.set_page_load_timeout(60)
            # driver.set_script_timeout(60)
            driver = False
            inventory_array = []
            asin_info_remove_array = []
            try:
                for i in range(0, len(asin_info_array)):
                    tmp_info = asin_info_array[i]
                    result = self.get_inventory_jp(driver, tmp_info['asin'], ips_array)
                    if result == False or result == -111:
                        asin_info_remove_array.append(asin_info_array[i])
                        tmp_info['status'] = 'err'
                        if driver != False:
                            driver.quit()
                            time.sleep(2)
                            chrome_options = webdriver.ChromeOptions()
                            prefs = {
                                'profile.default_content_setting_values': {
                                    'images': 2,
                                    'javascript': 2
                                }
                            }
                            chrome_options.add_experimental_option("prefs", prefs)
                            driver = webdriver.Chrome(chrome_options=chrome_options)
                            driver.set_page_load_timeout(60)
                            driver.set_script_timeout(60)
                    else:
                        tmp_info['shipping'] = result['shipping']
                        tmp_info['seller'] = result['seller']
                        tmp_info['qa'] = result['qa']
                        tmp_info['limited'] = result['limited']
                        if result['seller'] == 1:
                            inventory_array.append(copy.deepcopy(result))
                        else:
                            asin_info_remove_array.append(asin_info_array[i])

            except Exception as e:
                status = False
                amazonpage.window_capture('unknown-error')
                print(traceback.format_exc(), flush=True)
                print(str(e), flush=True)
            finally:
                if driver != False:
                    driver.quit()
                if status == False:
                    return False

            for i in range(0, len(asin_info_remove_array)):
                asin_info_array.remove(asin_info_remove_array[i])

            if len(asin_info_array) != len(inventory_array):
                print(len(asin_info_array), flush=True)
                print(len(inventory_array), flush=True)

            # print(len(asin_info_array), flush=True)
            # print(len(inventory_array), flush=True)
            # input("xxxx")
            # for i in range(0, len(asin_info_array)):
            #     with open('test.txt', 'a') as f:
            #         f.writelines(json.dumps(inventory_array[i], cls=DateEncoder) + "\n")
            #     print(inventory_array[i])
            #     with open('test.txt', 'a') as f:
            #         f.writelines(json.dumps(asin_info_array[i], cls=DateEncoder) + "\n")
            #     f.close()
            #     print(asin_info_array[i])

            amazondata = AmazonData()
            status = amazondata.create_database('amazondata')
            if status == True:
                status = amazondata.connect_database('amazondata')
                if status == True:
                    for i in range(0, len(asin_info_array)):
                        asin = asin_info_array[i]['asin']
                        # asin_info_table = node + '_' + type + '_' + asin
                        # status = amazondata.create_asin_info_table(asin_info_table)
                        # if status == True:
                        #     print("asin_info_table create sucessfully + " + asin_info_table, flush=True)
                        #     status = amazondata.insert_asin_info_data(asin_info_table, asin_info_array[i])
                        node_table = node + '_' + type
                        status = amazondata.create_node_table(node_table)
                        if status == True:
                            # print("node_table create sucessfully + " + node_table, flush=True)
                            status = amazondata.insert_node_data(node_table, asin_info_array[i])
                            if status == True:
                                # print("node_data inserted sucessfully.. + " + node_table, flush=True)
                                if asin_info_array[i]['limited'] == 'no' and asin_info_array[i]['status'] != 'err' and asin_info_array[i]['seller'] == 1:
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
                                                    'task_id': '1',
                                                    'last_date': cur_date,
                                                    'node_name': node_name
                                                }
                                                status = insert_task_node('SALE_TASK', task_data)
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

    def us_node_gather(self, url):
        item_prefix = "//*[@id=\'zg-ordered-list\']/li[position()="
        item_postfix = "]/span"
        price_symbol = ".//div/span/div[position()=2]/a[position()=1]/span/span"
        review_symbol = ".//div/span/div[position()=1]/a[position()=2]"
        href_symbol = ".//div/span/div[position()=2]/a[position()=1]"
        rate_symbol = ".//div/span/div[position()=1]/a"
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        try:
            #driver.get("https://www.amazon.com/gp/bestsellers/electronics/297859")
            driver.get(url)
            for i in range(1, 50):
                item_symbol = item_prefix + str(i) + item_postfix
                element = driver.find_element_by_xpath(item_symbol)
                price = element.find_element_by_xpath(price_symbol)
                price_text = price.text
                href = element.find_element_by_xpath(href_symbol)
                asin_text = getasinfromhref(href.get_attribute("href"))
                review = element.find_element_by_xpath(review_symbol)
                review_text = review.text
                rate = element.find_element_by_xpath(rate_symbol)
                rate_text = rate.get_attribute("title").split(" ")[0]
                tmp = asin_text + " " + price_text.strip('$') + " " + review_text.replace(',', '') + " " + rate_text
                print(tmp, flush=True)
        except NoSuchElementException as msg:
            print("Except: NoSuchElementException", flush=True)
        except Exception as e:
            print(e, flush=True)
        finally:
            driver.quit()

    def get_inventory_us(self, driver_upper, asin, ips_array):
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
            else:
                print("proxy ip is: " + ip, flush=True)
            proxyauth_plugin_path = utils.create_proxyauth_extension(
                proxy_host='zproxy.lum-superproxy.io',
                proxy_port=22225,
                proxy_username=user_prefix+ip,
                proxy_password='o9dagiaeighm'
            )
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
            print("get_inventory_us + " + asin, flush=True)
            url = 'https://www.amazon.com/dp/' + asin
            driver.get(url)
            amazonasinpage = AmazonAsinPage(driver)

            amazonasinpage.random_sleep(3000, 5000)

            if amazonasinpage.is_element_exsist(*INEXSISTED_FLAG_US):
                print("ASIN is unaccessible...", flush=True)
                return False

            if driver.title == "Amazon CAPTCHA" or amazonasinpage.is_element_exsist(*LOGO) == False:
                amazonwrapper.mark_unaccessible_ip(ip)
                status = -111
                return -111

            amazonasinpage.select_size(asin, 1000, 2000)

            if amazonasinpage.is_element_exsist(*FBA_FLAG):
                data['shipping'] = 'FBA'
            elif amazonasinpage.is_element_exsist(*AB_FLAG_US):
                element = driver.find_element(*AB_FLAG_US)
                if 'Ships from and sold by Amazon.com' in element.text:
                    print("sold by Amazon Basic..", flush=True)
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

            if amazonasinpage.is_element_exsist(*BUYER_COUNT):
                element = driver.find_element(*BUYER_COUNT)
                data['seller'] = int(getseller_us(element.text))

                # print("seller is: " + str(data['seller']))
                # print(element.text, flush=True)
            else:
                data['seller'] = 0

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
                                    print("check limited", flush= True)
                                    data['limited'] = 'yes'
                                    data['inventory'] = 0
                                else:
                                    # ss
                                    print(getsale_us(element.text), flush=True)
                                    input("yyyyy")
                                    data['inventory'] = int(getsale_us(element.text))
                                    print("inventory is: " + str(data['inventory']), flush=True)

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
                    amazonasinpage.window_capture(asin + '-nocart-')
        except NoSuchElementException as msg:
            status = False
            print("Except: NoSuchElementException", flush=True)
        except TimeoutException as msg:
            print("Except: TimeoutException", flush=True)
            amazonwrapper.mark_unaccessible_ip(ip)
            status = -111
        except Exception as e:
            status = False
            amazonasinpage.window_capture('unknown-error')
            print(traceback.format_exc(), flush=True)
            print(e, flush=True)
        finally:
            if driver_upper == False:
                driver.quit()
            return status

    def get_inventory_jp(self, driver_upper, asin, ips_array):
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
            else:
                print("proxy ip is: " + ip, flush=True)
            proxyauth_plugin_path = utils.create_proxyauth_extension(
                proxy_host='zproxy.lum-superproxy.io',
                proxy_port=22225,
                proxy_username=user_prefix+ip,
                proxy_password='o9dagiaeighm'
            )
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
                amazonwrapper.mark_unaccessible_ip(ip)
                status = -111
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
        except NoSuchElementException as msg:
            status = False
            print("Except: NoSuchElementException", flush=True)
        except TimeoutException as msg:
            print("Except: TimeoutException", flush=True)
            amazonwrapper.mark_unaccessible_ip(ip)
            status = -111
        except Exception as e:
            status = False
            amazonasinpage.window_capture('unknown-error')
            print(traceback.format_exc(), flush=True)
            print(e, flush=True)
        finally:
            if driver_upper == False:
                driver.quit()
            return status

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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
    # node = '2285178051'
    # type = 'BS'
    node = sys.argv[1]
    type = sys.argv[2]
    node_name = sys.argv[3]
    ips_array = amazonwrapper.get_all_accessible_ip()
    if ips_array == False:
        print("no accessible ip", flush=True)
        exit(-1)
    amazonspider = AmazonSpider()
    asin = 'B078RZVZ3T'
    # amazonspider.jp_node_gather(node, node_name, type, 3, ips_array)
    amazonspider.get_inventory_us(False, asin, ips_array)
    # asin_array = ['B077HLQ81K', 'B00FRDOCBS', 'B07BGXF6KF', 'B01LX9MVA0']
    # for i in range(0, 100):
    #     t1 = time.time()
    #     print("Testing <" + str(i) + '>', flush=True)
    #     get_inventory_jp(driver, asin_array[random.randint(0, (len(asin_array)) - 1)])
    #     time.sleep(random.randint(3, 5))
    #     t2 = time.time()
    #     print("总耗时：" + format(t2 - t1))
    #     print("Test End\n", flush=True)
    # get_inventory_jp(False, "B06ZXXQ54K")
    # driver.quit()