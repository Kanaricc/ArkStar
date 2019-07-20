import logging
from logging import debug,info
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
        debug('press start button')
        self.adb.tap(rand_pos(*unpack(config.pointdata['battle']['startAction'])))
        sleep(rd())
        
        # 理智归零
        debug('find if san is not enough')
        self.adb.pull_screenshot()
        button=image.match_img('./screenshot.png','./flag/flag_useorigin.png',0.8)
        if len(button)>0:
            if useorigin:
                self.adb.tap(rand_pos(button[0],delta=5))
                sleep(rd())
            else:
                info('out of san and no origin stone to use, stop tasks.')
                return False


        debug('confirm battle')
        self.adb.tap(rand_pos(*unpack(config.pointdata['battle']['confirmAction'])))
        while True:
            sleep(randint(10,15))
            debug('getting screenshot')
            self.adb.pull_screenshot()
            if len(image.match_img('./screenshot.png','./flag/flag_endbattle.jpg',0.8))>0:
                debug('battle endding flag detected, end battle')
                self.adb.tap(rand_pos(config.pointdata['battle']['confirmResult'],delta=100))
                break
        sleep(rd())
        return True
        
