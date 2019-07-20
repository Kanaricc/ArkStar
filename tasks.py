from adbshell import rand_pos,sleep
import config
import adbshell
import image
from config import unpack
from random import randint

class Task:
    def __init__(self,adb):
        self.__adb=adb
        pass
    
    def act(self):
        raise NotImplementedError

def rd(low=1200,high=2000):
    return randint(low,high)/1000

class StartBattleTask:
    def __init__(self,adb):
        self.adb=adb
    
    def act(self,useorigin=False):
        print("press start")
        self.adb.tap(rand_pos(*unpack(config.pointdata['battle']['startAction'])))
        sleep(rd())
        
        # 理智归零
        self.adb.pull_screenshot()
        button=image.match_img('./screenshot.png','./flag/flag_useorigin.png',0.8)
        if len(button)>0:
            if useorigin:
                self.adb.tap(rand_pos(button[0],delta=5))
                sleep(rd())
            else:
                print("out of san")
                return


        print('press confirm')
        self.adb.tap(rand_pos(*unpack(config.pointdata['battle']['confirmAction'])))
        while True:
            sleep(randint(10,15))
            print('getting screenshot')
            self.adb.pull_screenshot()
            if len(image.match_img('./screenshot.png','./flag/flag_endbattle.jpg',0.8))>0:
                print('end detected')
                self.adb.tap(rand_pos(config.pointdata['battle']['confirmResult'],delta=100))
                break
        
