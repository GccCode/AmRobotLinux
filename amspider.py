#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import re
import sys
import io
from selenium.webdriver.common.by import By
from amazonasinpage import AmazonAsinPage
from selenium.common.exceptions import NoSuchElementException
from amazonpage import AmazonPage

BUYER_COUNT = (By.XPATH, '//*[@id=\'olp_feature_div\']/div/span[position()=1]/a')
QA_COUNT = (By.XPATH, '//*[@id=\'askATFLink\']/span')
FBA_FLAG = (By.ID, "SSOFpopoverLink")
NO_THANKS = (By.ID, 'attachSiNoCoverage')
VIEW_CART_BUTTON = (By.ID, 'attach-sidesheet-view-cart-button')
VIEW_CART_BUTTON1 = (By.ID, 'hlb-view-cart')
ITEM_SELECT_US = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/span[position()=1]/select')
ITEM_INPUT_US = (By.XPATH,
                          '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/input')
ITEM_SUBMIT_US = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/div/span/span')
INVENTORY_TIPS_US = (By.XPATH,
                              '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div[position()=1]/div/div/div/span')
ITEM_DELETE_US = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=2]/div[position()=1]/div[position()=4]/div[position()=2]/div[position()=1]/div/div/div[position()=2]/div/span[position()=1]/span')

PRODUCT_ITEM_JP = (By.XPATH,
                        '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]')
ITEM_SELECT_JP = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/span[position()=1]/select[position()=1]')
ITEM_INPUT_JP = (By.XPATH,
                          '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]/div[position()=4]/div/div[position()=3]/div/div[position()=1]/input[position()=1]')
ITEM_SUBMIT_JP = (By.ID, 'a-autoid-1')
INVENTORY_TIPS_JP = (By.XPATH,
                              '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]/div[position()=4]/div[position()=1]/div/div/div/span')
ITEM_DELETE_JP = (By.XPATH,
                           '//*[@id=\'activeCartViewForm\']/div[position()=1]/div[position()=1]/div[position()=2]/div/div/div[position()=1]/div[position()=4]/div[position()=2]/div[position()=1]/div/div/div[position()=2]/div/span[position()=1]')

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

def getasinfromhref(template):
    rule = r'dp/(.*?)/ref'
    slotList = re.findall(rule, template)
    return slotList[0]

def getimgidfromhref(template):
    rule = r'I/(.*?)\.'
    slotList = re.findall(rule, template)
    return slotList[0]

def jp_node_gather():
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    amazonpage = AmazonPage(driver)
    node = '2285178051'
    type = 'top'
    asin_info_data = {
        'rank'      : None,
        'asin'      : None,
        'node'      : node,
        'price'     : None,
        'review'    : None,
        'rate'      : None,
        'qa'        : 0,
        'shipping'  : None,
        'avg_sale'  : 0,
        'limited'   : 'no',
        'img_url'   : None
    }
    try:
        for page in range(0, 5):
            url = "https://www.amazon.co.jp/gp/bestsellers/electronics/2285178051#" + str(page + 1)
            driver.get(url)
            amazonpage.random_sleep(3000, 5000)
            print("Start gathering page: <" + str(page + 1) + "> ##########", flush=True)

            for i in range(0, 3):
                tmp_symbol = CRITICAL_TITLE_PREFIX + str(i + 1) + CRITICAL_TITLE_POSTFIX
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['asin'] = getasinfromhref(element.get_attribute('href'))
                    print("Asin is: " + asin_info_data['asin'], flush=True)

                tmp_symbol = CRITICAL_REVIEWS_PREFIX + str(i + 1) + CRITICAL_REVIEWS_POSTFIX
                has_review = amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol))
                if has_review:
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['review'] = int(element.text)
                    print("Review Count is: " + element.text, flush=True)
                    tmp_symbol = CRITICAL_RATE_PREFIX + str(i + 1) + CRITICAL_RATE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['rate'] = float(element.get_attribute('title').split(' ')[1])
                        print("Rate is: " + element.get_attribute('title').split(' ')[1], flush=True)
                else:
                    asin_info_data['review'] = 0
                    print("Review Count is: 0", flush=True)
                    asin_info_data['rate'] = 0
                    print("Rate is: 0", flush=True)
                if has_review:
                    tmp_symbol = CRITICAL_FBA_PREFIX + str(i + 1) + CRITICAL_FBA_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        asin_info_data['shipping'] = 'FBA'
                        print("FBA", flush=True)
                        tmp_symbol = CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX + str(i + 1) + CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX
                    else:
                        asin_info_data['shipping'] = 'FBM'
                        print("FBM", flush=True)
                        tmp_symbol = CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX + str(i + 1) + CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['price'] = int(element.text.strip('￥ ').replace(',', ''))
                        print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                else:
                    tmp_symbol = CRITICAL_FBA_PREFIX + str(i + 1) + CRITICAL_FBA_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        asin_info_data['shipping'] = 'FBA'
                        print("FBA", flush=True)
                        tmp_symbol = CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX + str(
                            i + 1) + CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX
                    else:
                        asin_info_data['shipping'] = 'FBM'
                        print("FBM", flush=True)
                        tmp_symbol = CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX + str(
                            i + 1) + CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['price'] = int(element.text.strip('￥ ').replace(',', ''))
                        print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)

                tmp_symbol = CRITICAL_IMGSRC_PREFIX + str(i + 1) + CRITICAL_IMGSRC_POSTFIX
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    #  https://images-na.ssl-images-amazon.com/images/I/61EHMhJe1YL._SL500_SR160,160_.jpg
                    asin_info_data['img_url'] = getimgidfromhref(element.get_attribute('src'))
                    print("ImgSrc is: " + element.get_attribute('src'), flush=True)

                tmp_symbol = CRITICAL_RANK_PREFIX + str(i + 1) + CRITICAL_RANK_POSTFIX + '2]'
                if page != 0:
                    tmp_symbol = CRITICAL_RANK_PREFIX + str(i + 1) + CRITICAL_RANK_POSTFIX + '1]'
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['rank'] = int(element.text.strip().replace('.', ''))
                    print("Top Rank is: " + element.text.strip().replace('.', ''), flush=True)

                print(asin_info_data)
                print("** ------------------- **", flush=True)

            for i in range(0, 17):
                tmp_symbol = NON_CRITICAL_TITLE_PREFIX + str(i + 1) + NON_CRITICAL_TITLE_POSTFIX
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['asin'] = getasinfromhref(element.get_attribute('href'))
                    print("Asin is: " + getasinfromhref(element.get_attribute('href')), flush=True)

                tmp_symbol = NON_CRITICAL_REVIEWS_PREFIX + str(i + 1) + NON_CRITICAL_REVIEWS_POSTFIX
                has_review = amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol))
                if has_review:
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['review'] = int(element.text)
                    print("Review Count is: " + element.text, flush=True)
                    tmp_symbol = NON_CRITICAL_RATE_PREFIX + str(i + 1) + NON_CRITICAL_RATE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['rate'] = float(element.get_attribute('title').split(' ')[1])
                        print("Rate is: " + element.get_attribute('title').split(' ')[1], flush=True)
                else:
                    asin_info_data['review'] = 0
                    print("Review Count is: 0", flush=True)
                    asin_info_data['rate'] = 0
                    print("Rate is: 0", flush=True)
                if has_review:
                    tmp_symbol = NON_CRITICAL_FBA_PREFIX + str(i + 1) + NON_CRITICAL_FBA_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        asin_info_data['shipping'] = "FBA"
                        print("FBA", flush=True)
                        tmp_symbol = NON_CRITICAL_HAS_REVIEW_FBA_PRICE_PREFIX + str(i + 1) + NON_CRITICAL_HAS_REVIEW_FBA_PRICE_POSTFIX
                    else:
                        asin_info_data['shipping'] = "FBM"
                        print("FBM", flush=True)
                        tmp_symbol = NON_CRITICAL_HAS_REVIEW_FBM_PRICE_PREFIX + str(i + 1) + NON_CRITICAL_HAS_REVIEW_FBM_PRICE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['price'] = int(element.text.strip('￥ ').replace(',', ''))
                        print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)
                else:
                    tmp_symbol = NON_CRITICAL_FBA_PREFIX + str(i + 1) + NON_CRITICAL_FBA_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        asin_info_data['shipping'] = "FBA"
                        print("FBA", flush=True)
                        tmp_symbol = NON_CRITICAL_NO_REVIEW_FBA_PRICE_PREFIX + str(
                            i + 1) + NON_CRITICAL_NO_REVIEW_FBA_PRICE_POSTFIX
                    else:
                        asin_info_data['shipping'] = "FBM"
                        print("FBM", flush=True)
                        tmp_symbol = NON_CRITICAL_NO_REVIEW_FBM_PRICE_PREFIX + str(
                            i + 1) + NON_CRITICAL_NO_REVIEW_FBM_PRICE_POSTFIX
                    if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                        element = driver.find_element_by_xpath(tmp_symbol)
                        asin_info_data['price'] = int(element.text.strip('￥ ').replace(',', ''))
                        print("Price is : " + element.text.strip('￥ ').replace(',', ''), flush=True)

                tmp_symbol = NON_CRITICAL_IMGSRC_PREFIX + str(i + 1) + NON_CRITICAL_IMGSRC_POSTFIX
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['img_url'] = getimgidfromhref(element.get_attribute('src'))
                    print("ImgSrc is: " + element.get_attribute('src'), flush=True)


                tmp_symbol = NON_CRITICAL_RANK_PREFIX + str(i + 1) + NON_CRITICAL_RANK_POSTFIX + '1]'
                if amazonpage.is_element_exsist(*(By.XPATH, tmp_symbol)):
                    element = driver.find_element_by_xpath(tmp_symbol)
                    asin_info_data['rank'] = int(element.text.strip().replace('.', ''))
                    print("Top Rank is: " + element.text.strip(), flush=True)
                print(asin_info_data)
                print("** ------------------- **", flush=True)
        amazonpage.random_sleep(2000, 5000)
    except NoSuchElementException as msg:
        print("Except: NoSuchElementException", flush=True)
    except Exception as e:
        print(e, flush=True)
    finally:
        input("waiting.....")
        driver.quit()

def us_node_gather(url):
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

def test_get_inventory_us():
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    try:
        # driver.get("https://www.amazon.com/dp/B078H7VY19")
        driver.get("https://www.amazon.com/dp/B079NNC8N8")
        amazonasinpage = AmazonAsinPage(driver)
        if amazonasinpage.is_element_exsist(*FBA_FLAG):
            print("product is fba...", flush=True)
        else:
            print("product is fbm or not exsist...", flush=True)

        amazonasinpage.random_sleep(1000, 2000)
        if amazonasinpage.is_element_exsist(*QA_COUNT):
            element = driver.find_element(*QA_COUNT)
            print(element.text)
        else:
            print("qa_count not exsist...", flush=True)

        if amazonasinpage.is_element_exsist(*BUYER_COUNT):
            element = driver.find_element(*BUYER_COUNT)
            print(element.text)
        else:
            print("buy count no no", flush=True)

        amazonasinpage.add_cart(8000, 10000)

        if amazonasinpage.is_element_exsist(*NO_THANKS) == True:
            amazonasinpage.click(*NO_THANKS)

        amazonasinpage.random_sleep(1000, 2000)
        if amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON):
            amazonasinpage.click(*VIEW_CART_BUTTON)
            amazonasinpage.random_sleep(8000, 10000)
        elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON1):
            amazonasinpage.click(*VIEW_CART_BUTTON1)
            amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.select(9, *ITEM_SELECT_US)
        amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.input("999", *ITEM_INPUT_US)
        amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.click(*ITEM_SUBMIT_US)
        amazonasinpage.random_sleep(8000, 10000)

        element = driver.find_element(*INVENTORY_TIPS_US)
        print(element.text)

        amazonasinpage.click(*ITEM_DELETE_US)
    except NoSuchElementException as msg:
        print("Except: NoSuchElementException", flush=True)
    except Exception as e:
        print(e, flush=True)
    finally:
        input("xxx")
        driver.quit()

def test_get_inventory_jp(): # driver, asin):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    try:
        # url = 'ttps://www.amazon.co.jp/dp/' + asin
        driver.get("https://www.amazon.co.jp/dp/B07BGXF6KF")
        amazonasinpage = AmazonAsinPage(driver)
        if amazonasinpage.is_element_exsist(*FBA_FLAG):
            print("product is fba...", flush=True)
        else:
            print("product is fbm or not exsist...", flush=True)

        amazonasinpage.random_sleep(1000, 2000)
        if amazonasinpage.is_element_exsist(*QA_COUNT):
            element = driver.find_element(*QA_COUNT)
            print(element.text)
        else:
            print("qa_count not exsist...", flush=True)

        if amazonasinpage.is_element_exsist(*BUYER_COUNT):
            element = driver.find_element(*BUYER_COUNT)
            print(element.text)
        else:
            print("buy count no no", flush=True)

        amazonasinpage.add_cart(8000, 10000)

        if amazonasinpage.is_element_exsist(*NO_THANKS) == True:
            amazonasinpage.click(*NO_THANKS)

        amazonasinpage.random_sleep(1000, 2000)
        if amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON):
            amazonasinpage.click(*VIEW_CART_BUTTON)
            amazonasinpage.random_sleep(8000, 10000)
        elif amazonasinpage.is_element_exsist(*VIEW_CART_BUTTON1):
            amazonasinpage.click(*VIEW_CART_BUTTON1)
            amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.select(9, *ITEM_SELECT_JP)
        amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.input("999", *ITEM_INPUT_JP)
        amazonasinpage.random_sleep(8000, 10000)

        amazonasinpage.click(*ITEM_SUBMIT_JP)
        amazonasinpage.random_sleep(8000, 10000)

        element = driver.find_element(*INVENTORY_TIPS_JP)
        print(element.text)

        amazonasinpage.click(*ITEM_DELETE_JP)
    except NoSuchElementException as msg:
        print("Except: NoSuchElementException", flush=True)
    except Exception as e:
        print(e, flush=True)
    finally:
        input("waiting....")
        driver.quit()

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    #jp_node_gather()
    test_get_inventory_jp()