import cv2 as cv
import numpy as np
import os
import subprocess

def match_img(image,target,value):
    img_rgb=cv.imread(image)
    img_gray=cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)
    template=cv.imread(target,0)
    #w,h=template.shape[::-1]
    res=cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold=value
    loc=np.where(res>=threshold)

    """
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb,pt,(pt[0]+w,pt[1]+h),(7,249,151),2)
    cv.imshow('de',img_rgb)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    ans=[]
    for pt in zip(*loc[::-1]):
        ans.append(pt)
    return ans

def detect_number(image_path):
    save_path="./t"
    p=subprocess.Popen(f"tesseract {image_path} {save_path} --psm 7", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdout.read()
    res=""
    with open(save_path+".txt") as f:
        res=f.readline()
    intres=0
    try:
        intres=int(res)
    except:
        return res
    return intres

