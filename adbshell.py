import os
import random
import json
from time import sleep



def rand_pos(posl,posr=None,delta=5):
    res=posl
    if posr!=None:
        res[0]=random.randint(posl[0],posr[0])
        res[1]=random.randint(posl[1],posr[1])
    else:
        res[0]=random.randint(posl[0]-delta,posl[0]+delta)
        res[1]=random.randint(posl[1]+delta,posl[1]+delta)
    return res

class ADBHelper:
    def __init__(self):
        pass

    def init_adb(self):
        print(self.runcmd('adb devices'))
    
    def runcmd(self,cmd):
        print(cmd)
        print(os.popen(cmd).read())

    def tap(self,pos,delay=0):
        if delay==0:
            self.runcmd(f"adb shell input tap {pos[0]} {pos[1]}")
        else:
            self.runcmd(f"adb shell input swipe {pos[0]} {pos[1]} {pos[0]} {pos[1]} {delay}")

    def pull_screenshot(self):
        self.runcmd('adb shell screencap -p /sdcard/screenshot.png')
        sleep(1)
        self.runcmd('adb pull /sdcard/screenshot.png ./')

if __name__=="__main__":
    pointdata=None
    with open('pointdata.json','r') as f:
        pointdata=json.load(f)
    
    adbhelper=ADBHelper()
    adbhelper.init_adb()