import logging
from logging import debug,info
from adbshell import sleep
import config
import adbshell
import image
from config import unpack,gconfig
from simuman import rand_normal,rand_pos

class InvalidParamException:
    pass

class TaskHelper:
    def __init__(self,adb):
        self.__adb=adb
        self.__tapdelay=gconfig['delay']['tap']
        self.__uidelay=gconfig['delay']['uidelay']
        pass
    
    def sleepui(self,times=1):
        sleep(rand_normal(*self.__uidelay)*times/1000)
    
    def tapdelay(self,pos):
        if(len(pos)==2):
            self.__adb.tap(pos,rand_normal(*self.__tapdelay))
        elif len(pos)==4:
            self.__adb.tap(rand_pos(*unpack(pos)),rand_normal(*self.__tapdelay))
        else:
            raise InvalidParamException

class StartBattleTask:
    def __init__(self,adb):
        self.__adb=adb
        self.__helper=TaskHelper(adb)
    
    def act(self,useorigin=False):
        debug('press start button')
        self.__helper.tapdelay(config.pointdata['battle']['startAction'])
        self.__helper.sleepui()
        
        # 理智归零
        debug('find if san is not enough')
        self.__adb.pull_screenshot()
        button=image.match_img('./screenshot.png','./flag/flag_useorigin.png',0.8)
        if len(button)>0:
            if useorigin:
                debug('use origin stone to fill san')
                self.__helper.tapdelay(button[0])
                self.__helper.sleepui()

                # 重新开始
                debug('press start button')
                self.__helper.tapdelay(config.pointdata['battle']['startAction'])
                self.__helper.sleepui()

            else:
                info('out of san and no origin stone to use, stop tasks.')
                return False


        debug('confirm battle')
        self.__helper.tapdelay(config.pointdata['battle']['confirmAction'])
        self.__helper.sleepui(1.5)

class ConfirmBattleResultTask:
    def __init__(self,adb):
        self.__adb=adb
        self.__helper=TaskHelper(adb)
    
    def act(self):
        while True:
            sleep(rand_normal(*gconfig['delay']['enddetect']))
            debug('getting screenshot')
            self.__adb.pull_screenshot()
            if len(image.match_img('./screenshot.png','./flag/flag_endbattle.jpg',0.8))>0:
                debug('battle endding flag detected, end battle')
                self.__helper.tapdelay(config.pointdata['battle']['confirmResult'])
                break
        self.__helper.sleepui(1.5)

class AutoBattleTask:
    def __init__(self,adb):
        self.__adb=adb
        self.__helper=TaskHelper(adb)
    
    def act(self,useorigin=False):
        if StartBattleTask(self.__adb).act(useorigin) == False:
            return False
        ConfirmBattleResultTask(self.__adb).act()

        return True
        
