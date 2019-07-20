from adbshell import ADBHelper
from tasks import *
import logging

def app():
    adbhelper=ADBHelper()
    adbhelper.init_adb()
    StartBattleTask(adbhelper).act()

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    app()
