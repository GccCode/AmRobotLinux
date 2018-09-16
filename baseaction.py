#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import time as tm
import pyautogui
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pyscreenshot as ImageGrab
import pexpect
import subprocess
import os


class BaseAction(object):
    def __init__(self, driver):
        self.driver = driver
        self.screen_width = pyautogui.size()[0]
        self.screen_heigth = pyautogui.size()[1]

    def window_capture(self, filename):
        self.random_sleep(3000, 5000)
        cc = time.gmtime()
        bmpname = str(cc[0]) + str(cc[1]) + str(cc[2]) + str(cc[3] + 8) + str(cc[4]) + str(cc[5]) + '.bmp'
        tmpname = filename + "-" + bmpname
        im = ImageGrab.grab((0, 60, 1024, 600))
        im.save(tmpname)

    def shell_sudo_command(self, cmd, passwd):
        child = pexpect.spawn(cmd)
        index = child.expect(['password', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline(passwd)

    def change_random_proxy(self):
        pass

    def change_random_resolution(self):
        linux_resolution = ["1024x768x8", "1366x768x8", "1280x768x8", "800x600x8", "1920x1080x8"]
        index = random.randint(0, (len(linux_resolution) - 1))
        stop_cmd = ["killall", "Xvfb"]
        subprocess.call(stop_cmd, shell=False)
        start_cmd = ["Xvfb", ":5", "-ac", "-screen", "0", linux_resolution[index]]
        subprocess.Popen(start_cmd, shell=False, stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))
        os.environ['DISPLAY'] = ":5"
        print("** 分辨率：" + str(pyautogui.size()), flush=True)
        self.random_sleep(2500, 3000)

    def change_mac_address(self, passwd):
        self.shell_sudo_command("sudo ifconfig eth0 down", passwd)
        self.random_sleep(1000, 1500)
        cmd = "sudo ifconfig eth0 hw ether " + self.generate_random_mac_address()
        self.shell_sudo_command(cmd, passwd)
        self.random_sleep(1000, 1500)
        self.shell_sudo_command("sudo ifconfig eth0 up", passwd)
        self.random_sleep(3000, 5500)

    def generate_random_mac_address(self):
        Maclist = []
        for i in range(1, 7):
            RANDSTR = "".join(random.sample("0123456789abcdef", 2))
            if i == 1:
                tmp = int(RANDSTR, 16)
                if tmp % 2 == 1:
                    tmp -= 1
                    hex_tmp = hex(tmp)
                    hex_tmp_str_lens = len(str(hex_tmp))
                    if hex_tmp_str_lens == 3:
                        hex_str = "0" + str(hex_tmp)[2]
                    else:
                        hex_str = str(hex_tmp)[2] + str(hex_tmp)[3]
                    Maclist.append(hex_str)
                else:
                    Maclist.append(RANDSTR)
            else:
                Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        return RANDMAC

    def is_element_exsist(self, *locator):
        status = True
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException as msg:
            status = False
        finally:
            return status

    def  wait_element_match(self, timeout, displayed, *locator):
        count = 0
        while count < timeout:
            status = self.is_element_exsist(*locator)
            if status == displayed:
                return True
            else:
                count += 1
                time.sleep(1)
        if displayed == True:
            print(("TIMEOUT - 目标元素并未找到。。。"), flush=True)
        else:
            print(("TIMEOUT - 目标元素并未消失。。。"), flush=True)

        return False

    def hover(self, *locator):
        element = self.driver.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def select(self, index, *locator):
        element = self.driver.find_element(*locator)
        self.random_sleep(1000, 2000)
        element.find_elements_by_tag_name("option")[index].click()

    def input(self, content, *locator):
        try:
            input_box = self.driver.find_element(*locator)
        except Exception as e:
            print(type(e))
        else:
            self.driver.set_page_load_timeout(1)
            self.driver.set_script_timeout(1)
            for character in content:
                try:
                    input_box.send_keys(character)
                    time.sleep(random.randint(100, 800) / 1000)  # pause for 0.3 seconds
                except Exception as e:
                    print(type(e))
                    try:
                        input_box.send_keys(character)
                        time.sleep(random.randint(100, 800) / 1000)  # pause for 0.3 seconds
                    except Exception as e:
                        print(type(e))
                        pass
                    finally:
                        pass
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)

    def random_sleep(self, begin, end):
        if end != 0:
            time.sleep(random.randint(begin, end) / 1000)

    def mouse_move(self, x, y):
        move_time = random.randint(100, 500) / 1000
        pyautogui.moveTo(x, y, move_time)

    def random_mouse_move(self):
        t1 = tm.time()
        move_count = 0
        count = random.randint(1, 3)
        while move_count < count:
            x = random.randint(0, int(self.screen_width / 3))
            y = random.randint(0, int(self.screen_heigth / 3)) + 200
            if (y > 0) and (y < 200):
                y = y + 200
            move_time = random.randint(1, 20) * 1000 / 10000
            pyautogui.moveTo(x, y, move_time)
            self.random_sleep(500, 1500)
            move_count += 1

        t2 = tm.time()
        # print("random_mouse_move-总耗时：" + format(t2 - t1))

    def random_mouse_scoll(self):
        t1 = tm.time()
        scroll_count = 0
        count = random.randint(1, 3)
        tmp = random.randint(1, 2)
        if tmp == 1:
            direction = -1
        else:
            direction = 1
        while scroll_count < count:
            self.mouse_scoll(direction)
            self.random_sleep(500, 1500)
            scroll_count += 1

        t2 = tm.time()
        # print("random_mouse_scroll-总耗时：" + format(t2 - t1))

    def mouse_scoll(self, direction):
        scroll_count = random.randint(1, 10)
        pyautogui.scroll(scroll_count * direction)

    def enter_back(self):
        return

    def page_reload(self):
        return

    def scoll_to_top(self):
        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execut_script(js)