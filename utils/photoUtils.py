import cv2
import numpy as np

class PhotoSearcher:
    def __init__(self,imgPath,targetPath):
        self.imgPath = imgPath
        self.targetPath = targetPath

    def search(self):
        img_rgb = cv2.imread(self.imgPath)
        img_target = cv2.imread(self.targetPath)
        w, h = img_target.shape[:-1]

        res = cv2.matchTemplate(img_rgb, img_target, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb,pt,(pt[0]+h,pt[1]+w),(0,0,255),2)
            return pt[0]+h/2,pt[1]+w/2
        return


def findPosition(imgPath,targetPath):
    mySearcher = PhotoSearcher(imgPath,targetPath)
    try:
        x,y = mySearcher.search()
        return x,y
    except:
        return -1,-1

