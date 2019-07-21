from adbshell import ADBHelper
from tasks import *
import logging
import fire
from simuman import rand
import simuman

class DropDetector:
    def __init__(self,img_path):
        self.__path=img_path
    
    
class CommandLineApp:
    def __init__(self):
        self.__adbhelper=ADBHelper()
        self.__adbhelper.init_adb()
        simuman.generate_normaloffset()
    def autobattle(self,repeat=1,fillsan=False):
        """
        automatically enter and repeat one single boring battle again and again.
        """
        for i in range(repeat):
            info(f"repeat tasks #{i}")
            if AutoBattleTask(self.__adbhelper).act(fillsan) == False:
                logging.warning('tasks ended unexpectedly.')
                break
            sleep(rand_normal(5,9))

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CommandLineApp)
