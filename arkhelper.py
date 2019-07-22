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
from config import gconfig
import uuid

def lookup_name_by_uuid(id):
    if id not in gconfig['items-dict']:
        return id
    return gconfig['items-dict'][id]

class DropDetector:
    def __init__(self,flags_path):
        self.__flags_path=flags_path
        self.reload_flags()
    
    def reload_flags(self):
        self.__flags=[]
        self.__uuid=[]
        for parent, dirnames, filenames in os.walk(self.__flags_path,  followlinks=True):
            for filename in filenames:
                fullpath=os.path.join(self.__flags_path,filename)
                img=cv.imread(fullpath,0)
                debug('loading flags '+fullpath)
                if img is not None:
                    self.__uuid.append(filename.split('.')[0])
                    self.__flags.append(img) # 0,以灰度读取
        info(f"finish loading flags")
        debug(self.__flags)

        # 同步到config的数据库中
        for i in self.__uuid:
            if i not in gconfig['items-dict']:
                gconfig['items-dict'][i]=i
        config.save()
    
    def match_img(self,image,target,value):
        #w,h=template.shape[::-1]
        res=cv.matchTemplate(image,target,cv.TM_CCOEFF_NORMED)
        threshold=value
        loc=np.where(res>=threshold)
        ans=[]
        for pt in zip(*loc[::-1]):
            ans.append(pt)
        return ans
    
    def get_item_box(self,img):
        return img.crop((665+30,785,1920,975))
    
    def get_spliting_lines(self,img):
        #high=image.binarify(img,75)
        high=ImageEnhance.Contrast(img).enhance(2.6)
        #high.save('./debug.png','png')
        w,h=high.size
        breakpoints=[]
        black=0
        for x in range(0,w):
            r,g,b,al=high.getpixel((x,95)) # 物品中线为95
            if r!=0 or g!=0 or b!=0:
                if black>=25:
                    breakpoints.append(x)
                    #pass
                black=0
            if r==0 and g==0 and b==0:
                black+=1
        black=0
        for x in range(w-1,0,-1):
            r,g,b,al=high.getpixel((x,95)) # 物品中线为95
            if r!=0 or g!=0 or b!=0:
                if black>=25:
                    breakpoints.append(x)
                black=0
            if r==0 and g==0 and b==0:
                black+=1
        breakpoints.sort()

        #debug
        #draw=ImageDraw.Draw(high)
        #for x in breakpoints:
        #    draw.line((x,0,x,h),255)
        
        #high.save('./debug.png','png')
        return breakpoints
    
    def split_items(self,img):
        """
        将box中的物品切分
        并不会转为灰度
        """
        w,h=img.size
        #物品切分线
        breakpoints=self.get_spliting_lines(img)
        debug("borders of item:")
        debug(breakpoints)

        drops=[]
        for i in range(0,len(breakpoints),2):
            temp=img.crop((breakpoints[i],0,breakpoints[i+1],h))
            drops.append(temp)
        info(f"detect {len(drops)} items.")
        return drops

    def _split_item_number(self,img):
        threshold = 180
        table = []
        for i in range(256):
            if i < threshold:
                table.append(1)
            else:
                table.append(0)
        num=img.crop((90,135,155,168)).convert('L')
        #num=drops[0].convert('L')
        #num=ImageEnhance.Contrast(num).enhance(1.5)
        num=num.point(table,'1')
        return num
    
    def detect_item_number(self,img):
        self._split_item_number(img).save('./temp.png','png')
        return image.detect_number('./temp.png')

    def get_items_from_screenshot(self,img):
        im=img
        try:
            im+''
        except:
            pass
        else:
            info(f"open image at {im}")
            im=Image.open(im)
           
        drop=self.get_item_box(im)
        
        drops=self.split_items(drop)
        return drops
    def collect_database(self,img_path):
        drops=self.get_items_from_screenshot(img_path)

        cnt=0
        for item in drops:
            ex=self.detect_uuid(item)
            if ex is None:
                cnt+=1
                item.convert('L').crop((30,30,100,135)).save(os.path.join(self.__flags_path,f"{str(uuid.uuid4())}.jpg"),'jpeg')
        
        info(f"add unseen {cnt} items.")
        self.reload_flags()
    
    def detect_uuid(self,img):
        debug('turn img into gray')
        gray=cv.cvtColor(np.asarray(img),cv.COLOR_RGB2BGR)
        gray=cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
        debug('looking img up in current flags')
        for i in range(0,len(self.__flags)):
            if len(self.match_img(gray,self.__flags[i],0.8))>0:
                return self.__uuid[i]
        return None
    
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
    def __collect_items_saving_database(self,img_path,flags_path='./flags/items'):
        detector=DropDetector(flags_path)
        detector.collect_database(img_path)
    
    def collect_items(self,img_path,flags_path='./flags/items',auto_addition=True):
        detector=DropDetector(flags_path)
        if os.path.isfile(img_path):
            if auto_addition:
                detector.collect_database(img_path)
            drops=detector.get_items_from_screenshot(img_path)
            for item in drops:
                print(lookup_name_by_uuid(detector.detect_uuid(item)),detector.detect_item_number(item))
        else:
            ans={}
            for parent, dirnames, filenames in os.walk(img_path,followlinks=True):
                for filename in filenames:
                    fullpath=os.path.join(img_path,filename)
                    if not fullpath.endswith('.png'):continue
                    debug(f"open screenshot at {fullpath}")
                    if auto_addition:
                        detector.collect_database(fullpath)
                    drops=detector.get_items_from_screenshot(fullpath)
                    for item in drops:
                        uu=detector.detect_uuid(item)
                        if uu not in ans:
                            ans[uu]=0
                        number=detector.detect_item_number(item)
                        if isinstance(number,int):
                            ans[uu]+=detector.detect_item_number(item)
                        else:
                            logging.warning(f"number detect failed: get result: {number}. saving failed image")
                            copyfile('./temp.png',f"./failed_{lookup_name_by_uuid(uu)}_{str(uuid.uuid4())}.png")
            for k in ans:
                print(lookup_name_by_uuid(k),ans[k])

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(CommandLineApp)
