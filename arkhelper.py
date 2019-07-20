from adbshell import ADBHelper
from tasks import *
import logging
import fire
from simuman import rand

class CommandLineApp:
    def __init__(self):
        self.__adbhelper=ADBHelper()
        self.__adbhelper.init_adb()
    def autobattle(self,repeat=1,fillsan=False):
        """
        auto enter and repeat one single boring battle again and again.
        """
        for i in range(repeat):
            info(f"repeat tasks #{i}")
            if StartBattleTask(self.__adbhelper).act(fillsan) == False:
                logging.warning('tasks ended unexpectedly.')
                break
            sleep(rand(5,9))

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CommandLineApp)
