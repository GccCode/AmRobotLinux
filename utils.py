import subprocess
import random
import os


def change_random_resolution():
        linux_resolution = ["1024x768x8", "1366x768x8", "1280x768x8", "800x600x8", "1920x1080x8"]
        index = random.randint(0, (len(linux_resolution) - 1))
        stop_cmd = ["killall", "Xvfb"]
        ret = subprocess.call(stop_cmd, shell=False)
        start_cmd = ["Xvfb", ":5", "-ac", "-screen", "0", linux_resolution[index]]
        ret = subprocess.Popen(start_cmd, shell=False, stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))
        os.environ['DISPLAY'] = ":5"

# if __name__ == "__main__":
#     change_random_resolution()