from clients import conf,log
import PIL.ImageGrab
import cv2
import numpy as np
import time
import win32api, win32con, win32gui
import mouse
import easyocr

class PhotoSearch:
    def __init__(self,imgPath,targetPath):
        self.imgPath = imgPath
        self.targetPath = targetPath

    def search(self):
        img_rgb = cv2.imread(self.imgPath)
        img_target = cv2.imread(self.targetPath)
        h,w = img_target.shape[:-1]
        res = cv2.matchTemplate(img_rgb,img_target,cv2.TM_CCOEFF_NORMED)

        threshold = 0.9
        loc = np.where(res >= threshold)
        x,y = *loc[::-1][0]+w/2,*loc[::-1][1]+h/2

        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(img_rgb,pt,(pt[0]+w,pt[1]+h),(0,0,255),2)
        # cv2.imwrite("./img.png",img_rgb)
        return x,y


class PhotoRecognize:
    def __init__(self,imgPath):
        # 创建reader对象
        self.reader = easyocr.Reader(['en','ch_sim'])
        self.imgPath = imgPath

    def recognize(self):
        result = self.reader.readtext(self.imgPath)
        for i in result:
            print(i)

    def recognizeItemNum(self):
        pass

    #return number of item
    def recognizeNum(self):
        pass

    #return location of a level
    def recognizeLevel(self):
        pass


class MouseController:
    def __init__(self):
        self.m = mouse

    def draw(self,func):
        def warpFunc():
            self.hold()
            func()
            self.release()
        return warpFunc

    def moveToLeft(self,distance):
        self.draw(self.move(-distance,0))()

    def moveToRight(self,distance):
        self.draw(self.move(distance, 0))()

    def moveToUp(self,distance):
        self.draw(self.move(0, distance))()

    def moveToDown(self,distance):
        self.draw(self.move(0, -distance))()

    def move(self,x,y):
        self.m.move(x,y)

    def moveRelativeToWindow(self,x,y):
        pass

    def leftClick(self):
        self.m.click('left')

    def hold(self):
        self.m.press('left')

    def getPostion(self):
        return self.m.get_position()

    def release(self):
        self.m.release('left')

class WindowManipulator:
    def __init__(self,name,screenShotPath):
        self.logger = log.LoggingFactory.logger(__name__)

        self.name = name
        self.handle = win32gui.FindWindow(0, name)
        self.screenShotPath = screenShotPath
        if self.handle == 0:
            self.logger.fatal("Can't find screen")
            exit(0)


    def setWindowForeground(self):
        win32gui.SetForegroundWindow(self.handle)

    def getWindowPos(self):
        return  win32gui.GetWindowRect(self.handle)

    def getWindowLeftUpCornerPos(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.handle)
        return x1,y1

    def screenShotForWindow(self):
        startTime = time.time()
        myTime = time.localtime(startTime)
        timeName = str(myTime.tm_mon) + "_" + str(myTime.tm_mday) + "_" + str(myTime.tm_hour) + "_" + str(
            myTime.tm_min) + "_" + str(myTime.tm_sec) + ".png"
        imgName = self.screenShotPath + timeName
        myImg = PIL.ImageGrab.grab(bbox=(self.getWindowPos()),all_screens=True)
        myImg.save(imgName)
        self.logger.info("image save succeed||path=%s||spendTime=%sSecond",imgName,time.time()-startTime)
        return imgName


class Controller:
    def __init__(self):
        pass

    def run(self):
        pass

def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])

    window = WindowManipulator(Myconfig["window"]["name"],Myconfig["img"]["path"])

    photoPath = window.screenShotForWindow()
    myMouse = MouseController()

    # recoter = PhotoRecognize(photoPath)
    # recoter.recognize()
    searcher = PhotoSearch(photoPath,"./imgs/items/startOperation.png")
    moveX,moveY = searcher.search()
    x1,y1 = window.getWindowLeftUpCornerPos()
    myMouse.move(x1+moveX,y1+moveY)
    myMouse.leftClick()
    print(x1+moveX,y1+moveY)

    searcher = PhotoSearch(photoPath,"./imgs/items/starOperationInOperatorView.png")
    moveX, moveY = searcher.search()
    x1, y1 = window.getWindowLeftUpCornerPos()
    myMouse.move(x1 + moveX, y1 + moveY)


if __name__ == "__main__":
    main()
