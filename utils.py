import subprocess
import os
import threading
import pexpect
import pyscreenshot as ImageGrab
import random
import urllib3
import time
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import re
import configparser
from selenium import webdriver
import string
import zipfile
import datetime
import amazonwrapper


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
    line = random.randint(1, (getfilelines(filename) - 1))
    return readtline(
        filename,
        line,
    ).decode().strip().title()

def change_proxy():
    cur_cwd = os.getcwd()
    os.chdir("D:\Program Files\911S5 2018-05-23 fixed\ProxyTool")
    # os.popen("Autoproxytool.exe -changeproxy/US/CA")
    if is_proxy_file_exist() == False:
        os.popen("Autoproxytool.exe -changeproxy/US/CA")
    else:
        ip = getrandomproxy()
        cmd = "Autoproxytool.exe -changeproxy/ -ip=" + ip
        os.popen(cmd)
    os.chdir(cur_cwd)
    time.sleep(5)
    print(("* Switch ip from 911.re"), flush=True)


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """代理认证插件

    args:
        proxy_host (str): 你的代理地址或者域名（str类型）
        proxy_port (int): 代理端口号（int类型）
        proxy_username (str):用户名（字符串）
        proxy_password (str): 密码 （字符串）
    kwargs:
        scheme (str): 代理方式 默认http
        plugin_path (str): 扩展的绝对路径

    return str -> plugin_path
    """

    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def chrome_proxy_setup(option):
    proxy_line = getrandomline("proxy.txt")
    print("proxy_line is : " + proxy_line, flush=True)
    ip, port, username, passwd = proxy_line.split(":")
    # print("ip : " + ip.lower(), flush=True)
    # print("port : " + port, flush=True)
    # print("username : " + username.lower(), flush=True)
    # print("passwd : " + passwd.lower(), flush=True)
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=ip.lower(),
        proxy_port=int(port),
        proxy_username=username.lower(),
        proxy_password=passwd.lower()
    )
    option.add_extension(proxyauth_plugin_path)
    return ip.lower(), port, username.lower(), passwd.lower()

def chrome_proxy_setup_luminati(option):
    proxy_line = getrandomline("proxy.txt")
    print("proxy_line is : " + proxy_line, flush=True)
    ip, port, username, passwd = proxy_line.split(":")
    # print("ip : " + ip.lower(), flush=True)
    # print("port : " + port, flush=True)
    # print("username : " + username.lower(), flush=True)
    # print("passwd : " + passwd.lower(), flush=True)
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=ip.lower(),
        proxy_port=int(port),
        proxy_username=username.lower(),
        proxy_password=passwd.lower()
    )
    option.add_extension(proxyauth_plugin_path)
    return ip.lower(), port, username.lower(), passwd.lower()

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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxy_line = getrandomline("proxy.txt")
    ip, port, username, passwd = proxy_line.split(":")
    proxy_dict = {
        "http": "http://" + username.lower() + ":" + passwd.lower() + "@" + ip.lower() + ":" + port.lower(),
        "https": "https://" + username.lower() + ":" + passwd.lower() + "@" + ip.lower() + ":" + port.lower()
    }
    text = requests.get(url, headers=header, proxies=proxy_dict).text
    soup = BeautifulSoup(text, 'lxml')
    info = soup.find_all('input')
    lens = len(info)
    if lens == 0:
        return False
    # for i in range(0, 25):
    #     print(str(i) + " : " + info[i]['value'], flush=True)
    # name_phone = info[0]['value'] + '#' + info[9]['value']
    # name_visa = info[0]['value'] + '#' + info[11]['value'] + '#' + info[13]['value']
    return [info[5]['value'], info[22]['value'], info[24]['value']]

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
    if cardinfo == False:
        print(("* Generate Info In Failure..."), flush=True)
        return False
    phonenumber = cardinfo[0]
    cf_info.set("bill_address", "phone", phonenumber)
    cf_info.add_section("cardinfo")
    cardnumber = cardinfo[1]
    cf_info.set("cardinfo", "cardnumber", cardnumber)
    validmonth = cardinfo[2].split('/')[0]
    # validmonth = str(random.randint(1, 12))
    cf_info.set("cardinfo", "month", validmonth)
    validyear = cardinfo[2].split('/')[1]
    if int(validyear) < 2019:
        validyear = "2019"
    # validyear = str(random.randint(2019, 2025))
    cf_info.set("cardinfo", "year", validyear)

    cf_info.write(open('info.txt', 'w'))
    print(("* Generate Info Sucessfully..."), flush=True)
    return True

def generate_info_file_jp():
    cf_info = configparser.ConfigParser()
    cf_info.add_section("account")
    cf_info.set("account", "country", "us")
    username = generate_username()
    cf_info.set("account", "username", username)
    email = generate_email()
    cf_info.set("account", "email", email)
    password = generate_password()
    cf_info.set("account", "password", password)
    cf_info.set("account", "pronunciation", username)

    cf_info.write(open('info.txt', 'w'))
    print(("* Generate Info Sucessfully..."), flush=True)
    return True

def customized_broswer_with_luminati(ips_array):
    option = webdriver.ChromeOptions()
    user_prefix = 'lum-customer-hl_ecee3b35-zone-shared_test_api-ip-'
    ip = amazonwrapper.get_ramdon_accessible_ip(ips_array)
    if ip == False:
        print("can't get accessible ip", flush=True)
        exit(-1)
    else:
        print("proxy ip is: " + ip, flush=True)
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host='zproxy.lum-superproxy.io',
        proxy_port=22225,
        proxy_username=user_prefix + ip,
        proxy_password='o9dagiaeighm'
    )
    option.add_extension(proxyauth_plugin_path)
    # option.add_argument('--no-sandbox')
    # option.add_argument('--disable-gpu')
    # option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    return driver

def customized_broswer():
    option = webdriver.ChromeOptions()
    index = random.randint(0, (len(useragentlist) - 1))
    useragent = "--user-agent=" + useragentlist[index]
    option.add_argument(useragent)
    proxy_line = getrandomline("proxy.txt")
    ip, port, username, passwd = proxy_line.split(":")
    # print("ip : " + ip.lower(), flush=True)
    # print("port : " + port, flush=True)
    # print("username : " + username.lower(), flush=True)
    # print("passwd : " + passwd.lower(), flush=True)
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=ip.lower(),
        proxy_port=int(port),
        proxy_username=username.lower(),
        proxy_password=passwd.lower()
    )
    option.add_extension(proxyauth_plugin_path)
    # option.add_argument('--no-sandbox')
    # option.add_argument('--disable-gpu')
    # option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=option)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver

def window_capture(filename):
    random_sleep(3000, 5000)
    cc = time.gmtime()
    bmpname = str(cc[0]) + str(cc[1]) + str(cc[2]) + str(cc[3] + 8) + str(cc[4]) + str(cc[5]) + '.bmp'
    tmpname = filename + "-" + bmpname
    im = ImageGrab.grab((60, 60, 1024, 600))
    im.save(tmpname)

def shell_sudo_command(cmd, passwd):
    child = pexpect.spawn(cmd)
    index = child.expect(['password', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        child.sendline(passwd)


def change_random_proxy(self):
    pass

def random_sleep(begin, end):
    if end != 0:
        time.sleep(random.randint(begin, end) / 1000)

def change_mac_address(passwd):
    shell_sudo_command("sudo ifconfig eth0 down", passwd)
    random_sleep(1000, 1500)
    cmd = "sudo ifconfig eth0 hw ether " + generate_random_mac_address()
    shell_sudo_command(cmd, passwd)
    random_sleep(1000, 1500)
    shell_sudo_command("sudo ifconfig eth0 up", passwd)
    random_sleep(3000, 5500)

def generate_random_mac_address():
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

def input_wait(tip, timeout):
    def input_func(context):
        context['data'] = input(tip)

    context = {'data': '0'}
    t = threading.Thread(target=input_func, args=(context,))
    t.start()
    t.join(timeout)
    return context.get('data')

def change_random_resolution():
        linux_resolution = ["1024x768x8", "1366x768x8", "1280x768x8", "800x600x8", "1920x1080x8"]
        index = random.randint(0, (len(linux_resolution) - 1))
        stop_cmd = ["killall", "Xvfb"]
        ret = subprocess.call(stop_cmd, shell=False)
        start_cmd = ["Xvfb", ":5", "-ac", "-screen", "0", linux_resolution[index]]
        ret = subprocess.Popen(start_cmd, shell=False, stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))
        os.environ['DISPLAY'] = ":5"
        time.sleep(5)

class Administrator():
    def __init__(self, taskfile):
        self.cf = configparser.ConfigParser()
        self.cf.read("task.txt")
        outputdir = self.cf.get("output","dir")

        self.task_cf = configparser.ConfigParser()
        self.task_cf.read(taskfile)
        self.taskfile = taskfile

        self.record_cf = configparser.ConfigParser()
        nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
        self.recordfile = outputdir + nowdate + "_" + taskfile
        if os.path.exists(self.recordfile) != True:
            file = open(self.recordfile, 'w')
            file.close()
        self.record_cf.read(self.recordfile)

    def record_tasks(self, keyword, asins):
        if len(asins) != 0:
            if self.record_cf.has_section(keyword) == False:
                self.record_cf.add_section(keyword)

            for i in range(0, len(asins)):
                if self.record_cf.has_option(keyword, asins[i]) == False:
                    self.record_cf.set(keyword, asins[i], "1")
                else:
                    count = int(self.record_cf.get(keyword, asins[i]))
                    count += 1
                    self.record_cf.set(keyword, asins[i], str(count))
            print(asins, flush=True)
            print("* Recording Task: ", flush=True)
            self.record_cf.write(open(self.recordfile, 'w'))

    def get_tasks(self):
        return self.task_cf.sections()

    def get_tasks_len(self):
        return len(self.get_tasks())

    def get_random_task(self):
        return self.get_tasks()[random.randint(0, (self.get_tasks_len() - 1))]

    def is_run_out(self, section):
        count = self.task_cf.get(section, "count")
        if int(count) <= 0:
            return True
        else:
            return False

    def get_whiteasin(self, section):
        if self.task_cf.has_option(section, "whiteasin"):
            return self.task_cf.get(section, "whiteasin")
        else:
            return False

    def get_blackasin(self, section):
        if self.task_cf.has_option(section, "blackasin"):
            return self.task_cf.get(section, "blackasin")
        else:
            return False

    def is_super_link(self, section):
        return self.task_cf.get(section, "link")

    def is_qa_submit_needed(self, section):
        return self.task_cf.get(section, "qa_submit")

    def is_qa_submit_image(self, section):
        return self.task_cf.get(section, "qa_submit_image")

    def get_qa_content(self, section):
        return self.task_cf.get(section, "content")

    def is_add_to_card_needed(self, section):
        return self.task_cf.get(section, "addcart")

    def is_add_wishlist_needed(self, section):
        return self.task_cf.get(section, "wishlist")

    def is_add_wishlist_image(self, section):
        return self.task_cf.get(section, "wishlist_image")

    def get_keyword(self, section):
        return self.task_cf.get(section, "keyword")

    def is_all_over(self):
        if len(self.task_cf.sections()) == 0:
            return True
        else:
            return False

    def delete_task(self, section):
        if self.is_run_out(section):
            self.task_cf.remove_section(section)
            self.task_cf.write(open(self.taskfile, 'w'))
            self.task_cf.read(self.taskfile)

    def finish_task(self, section):
        count = int(self.task_cf.get(section, "count"))
        count -= 1
        self.task_cf.set(section, "count", str(count))
        self.task_cf.write(open(self.taskfile, 'w'))
        if count <= 0:
            self.delete_task(section)

        print("* Finishing Task.... + " + str(count), flush=True)

if __name__ == "__main__":
    # generate_info_file()
    # change_random_resolution()
    # driver = customized_broswer()
    # driver.get("https://www.whatismyipaddress.com")
    # input("xxx")
    # driver.quit()
    admin = Administrator("click_task.txt")
    asins = ['a', 'b', 'c']
    admin.record_tasks("hello", asins)