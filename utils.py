import subprocess
import random
import time
import os
import threading
import pexpect
import pyscreenshot as ImageGrab


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

    context = {'data': 'default'}
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

if __name__ == "__main__":
    #change_random_resolution()
    tmp = input_wait("Please input: ", 5)
    print("input is: " + tmp)
    window_capture("shot")