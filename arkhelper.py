from adbshell import ADBHelper
from tasks import *

def app():
    adbhelper=ADBHelper()
    adbhelper.init_adb()
    StartBattleTask(adbhelper).act()
    adbhelper.pull_screenshot()

if __name__=="__main__":
    app()
