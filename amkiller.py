#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import string
import time
import requests
import sys
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re
import configparser
from selenium import webdriver
from amazonpage import AmazonPage
from amazonregisterpage import AmazonRegisterPage
from amazonaccountpage import AmazonAccountPage
from amazonaddresspage import AmazonAddressPage
from amazonpaymentpage import AmazonPaymentPage
from amazonsearchpage import  AmazonSearchPage
import os
import io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


#0)
#1) Chrome
#2) Firefox+Win7:
#3) Safari+Win7:
#4) Opera+Win7:
#5) IE+Win7+ie9：
#6) Win7+ie8：
#7) WinXP+ie8：
#8) WinXP+ie7：
#9) WinXP+ie6：
useragentlist = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows NT 6.1; rv:61.0) Gecko/20100101 Firefox/61.0'
]

def getfilelines(filename, eol='\n', buffsize=4096):
    """计算给定文件有多少行"""
    with open(filename, 'rb') as handle:
        linenum = 0
        buffer = handle.read(buffsize)
        while buffer:
            linenum += buffer.count(bytes(eol, encoding='utf-8'))
            buffer = handle.read(buffsize)
        return linenum


def readtline(filename, lineno, eol="\n", buffsize=4096):
    """读取文件的指定行"""
    with open(filename, 'rb') as handle:
        readedlines = 0
        buffer = handle.read(buffsize)
        while buffer:
            thisblock = buffer.count(bytes(eol, encoding='utf-8'))
            if readedlines < lineno < readedlines + thisblock:
                # inthisblock: findthe line content, and return it
                return buffer.split(bytes(eol, encoding='utf-8'))[lineno - readedlines - 1]
            elif lineno == readedlines + thisblock:
                # need continue read line rest part
                part0 = buffer.split(bytes(eol, encoding='utf-8'))[-1]
                buffer = handle.read(buffsize)
                part1 = buffer.split(bytes(eol, encoding='utf-8'))[0]
                return part0 + part1
            readedlines += thisblock
            buffer = handle.read(buffsize)
        else:
            raise IndexError


def getrandomproxy():
    return getrandomline("proxy.txt")

def is_proxy_file_exist():
    return os.path.exists("proxy.txt")

def getrandomline(filename):
    """读取文件的任意一行"""
    import random
    return readtline(
        filename,
        random.randint(0, getfilelines(filename)),
    ).decode().strip().title()

def change_proxy():
    pass

def generate_username():
    return (getrandomline('usernames') + " " + getrandomline('usernames'))


def generate_password():
    #candidates = string.digits + string.ascii_letters + '!@$%&*+-_'
    candidates = string.digits + string.ascii_letters + '!@'
    passwd = ''
    for i in range(random.randint(8, 14)):
        passwd += random.choice(candidates)

    return passwd


def generate_email():
    prefix = string.digits + string.ascii_lowercase
    postfix = ['@yahoo.com', '@outlook.com', '@hotmail.com', '@gmail.com']
    prefix_len = random.randint(5, 12)
    mail = ''
    for i in range(prefix_len):
        mail += random.choice(prefix)
    return (getrandomline('usernames') + mail + random.choice(postfix))



def generate_address():
    url = r'https://fakena.me/random-real-address/'
    referer = r'https://fakena.me'
    header = {'user-agent': generate_user_agent(), 'referer': referer}
    text = requests.get(url, headers=header, verify=False).text
    pattern = re.compile('<strong>(.+)<br>(.+)</strong>')
    result = re.findall(pattern, text)
    if result:  # sometimes the result is empty
        address_line = result[0][0]
        city, state_zip = result[0][1].split(',')
        state, zip = state_zip.split()
        format_addr = [address_line, city, state, zip]
        return format_addr
    else:
        return ''


def generate_card():
    url = r'http://www.fakeaddressgenerator.com/World/us_address_generator'
    referer = r'http://www.fakeaddressgenerator.com/World'
    header = {'user-agent': generate_user_agent(), 'referer': referer}
    text = requests.get(url, headers=header).text
    soup = BeautifulSoup(text, 'lxml')
    info = soup.find_all('input')
    # for i in range(0, 25):
    #     print(str(i) + " : " + info[i]['value'])
    # name_phone = info[0]['value'] + '#' + info[9]['value']
    # name_visa = info[0]['value'] + '#' + info[11]['value'] + '#' + info[13]['value']
    return [info[5]['value'], info[21]['value'], info[23]['value']]

def generate_info_file():
    cf_info = configparser.ConfigParser()
    cf_info.add_section("account")
    cf_info.set("account", "country", "us")
    username = generate_username()
    cf_info.set("account", "username", username)
    email = generate_email()
    cf_info.set("account", "email", email)
    password = generate_password()
    cf_info.set("account", "password", password)
    cf_info.add_section("bill_address")
    cf_info.set("bill_address", "fullname", username)
    address = generate_address()
    line = address[0]
    cf_info.set("bill_address", "addressline1", line)
    city = address[1]
    cf_info.set("bill_address", "city", city)
    state = address[2]
    cf_info.set("bill_address", "state", state)
    zipcode = address[3]
    cf_info.set("bill_address", "postalcode", zipcode)
    cardinfo = generate_card()
    phonenumber = cardinfo[0]
    cf_info.set("bill_address", "phone", phonenumber)
    cf_info.add_section("cardinfo")
    cardnumber = cardinfo[1]
    cf_info.set("cardinfo", "cardnumber", cardnumber)
    validmonth = cardinfo[2].split('/')[0]
    cf_info.set("cardinfo", "month", validmonth)
    validyear = cardinfo[2].split('/')[1]
    if int(validyear) < 2019:
        validyear = "2019"
    cf_info.set("cardinfo", "year", validyear)

    cf_info.write(open('info.txt', 'w'))
    print(("* 随机生成身份资料。。。"), flush=True)

def customized_broswer():
    option = webdriver.ChromeOptions()
    # index = random.randint(0, (len(useragentlist) - 1))
    # useragent = "--user-agent=" + useragentlist[index]
    # option.add_argument(useragent)
    driver =  webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver

class Administrator():
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read("click_task.txt")

    def get_tasks(self):
        return self.cf.sections()

    def get_tasks_len(self):
        return len(self.get_tasks())

    def get_random_task(self):
        return self.get_tasks()[random.randint(0, (self.get_tasks_len() - 1))]

    def is_run_out(self, section):
        count = self.cf.get(section, "count")
        if int(count) <= 0:
            return True
        else:
            return False


    def get_whiteasin(self, section):
        return self.cf.get(section, "whiteasin")

    def is_all_over(self):
        if len(self.cf.sections()) == 0:
            return True
        else:
            return False

    def delete_task(self, section):
        if self.is_run_out(section):
            self.cf.remove_section(section)
            self.cf.write(open('click_task.txt', 'w'))
            self.cf.read("click_task.txt")

    def finish_task(self, section):
        count = int(self.cf.get(section, "count"))
        count -= 1
        self.cf.set(section, "count", str(count))
        self.cf.write(open('click_task.txt', 'w'))
        if count <= 0:
            self.delete_task(section)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    cf = configparser.ConfigParser()
    cf.read("task.txt")
    min_time = cf.get("search", "view_time_min")
    max_time = cf.get("search", "view_time_max")
    admin = Administrator()
    count = 0
    while count < 1:#admin.is_all_over() == False:
        change_proxy()
        generate_info_file()
        keyword = admin.get_random_task()
        driver = customized_broswer()
        t1 = time.time()
        amazonpage = AmazonPage(driver)
        display = amazonpage.change_random_resolution()
        try:
            count = 40 #random.randint(1, 100)
            if count < 30:
                ## registeration
                amazonpage.enter_amazon_page(3000, 5000)
                amazonpage.enter_register_page(3000, 5000)
                registerpage = AmazonRegisterPage(driver)
                registerpage.register(5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 30:
                    ## add bill address
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_address_page(3000, 5000)
                    addresspage = AmazonAddressPage(driver)
                    addresspage.add_address("bill", 5000, 10000)
                tmp = random.randint(1, 100)
                if tmp < 30:
                    ## add payment
                    amazonpage.enter_account_page(3000, 5000)
                    accountpage = AmazonAccountPage(driver)
                    accountpage.enter_payment_page(3000, 5000)
                    paymentpage = AmazonPaymentPage(driver)
                    paymentpage.add_new_payment(5000, 10000)

            amazonpage.enter_amazon_page(3000, 5000)
            amazonpage.wait_searchbox_exsist()
            searchpage = AmazonSearchPage(driver)
            print(("* 开始搜索关键词。。。"), flush=True)
            amazonpage.search_asin(keyword, 5000, 8000)
            searchpage.click_random_products("B0756GYPNS")
            admin.finish_task(keyword)
            time.sleep(random.randint(min_time, max_time))
        except NoSuchElementException as msg:
            print(("* 找不到元素。。。"), flush=True)
        except TimeoutException as msg:
            print(("* 网页加载超时。。。"), flush=True)
        except:
            pass
        finally:
            t2 = time.time()
            print("总耗时：" + format(t2 - t1))
            driver.quit()
            display.stop()
        count += 1

    print("* 任务全部完成！！！！")

