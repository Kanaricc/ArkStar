import cv2 as cv
import numpy as np
import os
import subprocess
from PIL import Image
from logging import debug
import uuid

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

class SIFTHelper:
    def __init__(self,flags_path='./flags'):
        self.__sift=cv.xfeatures2d.SIFT_create()
        self.__matcher=cv.BFMatcher()
        self.__dimg=[]
        self.__flags=[]
        self.__locs=[]
        self.__uuid=[]
        self.__database_path=os.path.join(flags_path,'items')
        debug(f"set features path as {self.__database_path}")
        
        self.load_SIFT_from_database()

    def has_id(self,id):
        return id in self.__uuid

    def getSIFT(self,img):
        key_points, desc=self.__sift.detectAndCompute(img,None)
        return key_points,desc
    
    def get_SIFT_from_file(self,path):
        debug(f"load sift from {path}")
        locs,desc= self.getSIFT(cv.imread(path,0))
        return locs,desc
    
    def load_SIFT_from_file(self,id,path):
        locs,desc=self.get_SIFT_from_file(path)
        self.__flags.append(desc)
        self.__locs.append(locs)
        self.__uuid.append(id)
        self.__dimg.append(cv.imread(path))
    
    def load_SIFT_from_database(self):
        self.__flags=[]
        self.__locs=[]
        self.__uuid=[]
        self.__dimg=[]
        for parent, dirnames, filenames in os.walk(self.__database_path,followlinks=True):
            for filename in filenames:
                fullpath=os.path.join(self.__database_path,filename)
                self.load_SIFT_from_file(filename.split('.')[0],fullpath)
        debug('finish loading sift features')
    
    def sift_alignment(self,query,train,dist=0.6):
        matches=self.__matcher.knnMatch(query,train,k=2)

        good_matches=[]
        for m,n in matches:
            if m.distance < dist*n.distance:
                good_matches.append([m])
        debug(f"catch features {len(good_matches)}")
        return good_matches

    
    def sift_alignment_with_database(self,img,fac=10):
        key,desc=self.getSIFT(img)

        for i in range(0,len(self.__flags)):
            #debug('this sift', self.__flags[i])
            gm=self.sift_alignment(self.__flags[i],desc)
            match_img = cv.drawMatchesKnn( self.__dimg[i], self.__locs[i],img, key,
                                    gm, None, flags=2)
            cv.imwrite(f"./debug_match_{str(uuid.uuid4())}.png",match_img)
            if len(gm)>fac:
                return self.__uuid[i]
        
        return None



    def sift_alignment_d(self,image_1: str, image_2: str):
        """
            Aligns two images by using the SIFT features. 
    
            Step 1. The function first detects the SIFT features in I1 and I2.
            Step 2. Then it uses match(I1,I2) function to find the matched pairs between 
            the two images.
            Step 3. The matched pairs returned by Step 2 are potential matches based 
            on similarity of local appearance, many of which may be incorrect.
            Therefore, we do a ratio test to find the good matches.
    
            Reference: https://docs.opencv.org/3.4.3/dc/dc3/tutorial_py_matcher.html
    
            Parameters:
                image_1, image_2: filename as string
            Returns:
                (matched pairs number, good matched pairs number, match_image)
        """
        im1 = cv2.imread(image_1, cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread(image_2, cv2.IMREAD_GRAYSCALE)
    
        sift = cv2.xfeatures2d.SIFT_create()
        key_points_1, descriptors_1 = sift.detectAndCompute(im1, None)
        key_points_2, descriptors_2 = sift.detectAndCompute(im2, None)
    
        bf_matcher = cv2.BFMatcher()  # brute force matcher
        # matches = bf_matcher.match(descriptors_1, descriptors_2)  # result is not good
        matches = bf_matcher.knnMatch(descriptors_1, descriptors_2, k=2)
    
        # Apply ratio test
        good_matches = []
        for m,n in matches:
            if m.distance < 0.6 * n.distance:  # this parameter affects the result filtering
                good_matches.append([m])
    
        match_img = cv2.drawMatchesKnn(im1, key_points_1, im2, key_points_2,
                                    good_matches, None, flags=2)
        return len(matches), len(good_matches), match_img

#matches, good_matches, match_img = sift_alignment('../flags/items/240eef57-a173-427d-b040-8609a5cceb22.jpg', './screenshot.png')
#cv2.imwrite('match.png', match_img)
#print(matches,good_matches)

def binarify(img,fac=180,rev=0):
        threshold = fac
        table = []
        for i in range(256):
            if i < threshold:
                table.append(rev)
            else:
                table.append(rev^1)
        num=img.convert('L')
        num=num.point(table,'1')
        return num

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

