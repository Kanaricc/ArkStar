from adbshell import ADBHelper
from tasks import *
import logging
from logging import debug,info
import fire
from simuman import rand
import simuman
import cv2 as cv
import os
from PIL import Image,ImageEnhance,ImageDraw
import numpy as np

class DropDetector:
    def __init__(self,flags_path):
        self.__flags_path=flags_path
        self.reload_flags()
    
    def reload_flags(self):
        self.__flags=[]
        for parent, dirnames, filenames in os.walk(self.__flags_path,  followlinks=True):
            for filename in filenames:
                fullpath=os.path.join(self.__flags_path,filename)
                img=cv.imread(fullpath,0)
                debug('loading flags '+fullpath)
                if img is not None:
                    self.__flags.append(img) # 0,以灰度读取
        info(f"finish loading flags")
        debug(self.__flags)
    
    def match_img(self,image,target,value):
        #w,h=template.shape[::-1]
        res=cv.matchTemplate(image,target,cv.TM_CCOEFF_NORMED)
        threshold=value
        loc=np.where(res>=threshold)
        ans=[]
        for pt in zip(*loc[::-1]):
            ans.append(pt)
        return ans
    
    def collect(self,img_path):
        im=Image.open(img_path)
        info(f"open image path at {img_path}")
        debug(im)
        drop=im.crop((665,785,1920,975))
        
        #增强图像对比度
        high=ImageEnhance.Contrast(drop).enhance(100000)
        w,h=high.size
        
        #物品切分线
        breakpoints=[]
        black=0
        for x in range(0,w):
            r,g,b,alpha=high.getpixel((x,95)) # 物品中线为95
            if r!=0 or g!=0 or b!=0:
                if black>=30:
                    breakpoints.append(x)
                black=0
            if r==0 and g==0 and b==0:
                black+=1
        for x in range(w-1,0,-1):
            r,g,b,alpha=high.getpixel((x,95)) # 物品中线为95
            if r!=0 or g!=0 or b!=0:
                if black>=30:
                    breakpoints.append(x)
                black=0
            if r==0 and g==0 and b==0:
                black+=1

        breakpoints.sort()
        
        debug("detect spliting line:")
        debug(breakpoints)

        drops=[]
        for i in range(0,len(breakpoints),2):
            temp=drop.crop((breakpoints[i],0,breakpoints[i+1],h))
            
            # pillow向cv转化
            img=cv.cvtColor(np.asarray(temp),cv.COLOR_RGB2BGR)
            img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            ex=False
            for flag in self.__flags:
                if len(self.match_img(img,flag,0.8))>0:ex=True
            if not ex:
                drops.append(temp.convert('L'))

        info(f"detect {len(drops)} unseen items, adding to database.")
        
        # 获取flag
        for i in drops:
            i.crop((30,30,100,135)).save(os.path.join(self.__flags_path,f"{str(uuid.uuid4())}.jpg"),'jpeg')
        self.reload_flags()
    
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
    def collectitems(self,img_path,flags_path='./flags/items'):
        detector=DropDetector(flags_path)
        detector.collect(img_path)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(CommandLineApp)
