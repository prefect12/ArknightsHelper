from clients import conf,log
import PIL.ImageGrab
import cv2
import numpy as np
import time
import win32api, win32con, win32gui

class PhotoRecognize:
    def __init__(self,imgPath):
        self.imgPath = imgPath

    def reloadImg(self,imgPath):
        self.imgPath = imgPath

    def loadImg(self):
        # load image item
        pass

    def recognizeItemNum(self):
        pass

    #return number of item
    def recognizeNum(self):
        pass

    #return location of a level
    def recognizeLevel(self):
        pass


class MyMouse:
    def __init__(self):
        pass

    def draw(self):
        pass

    def moveTo(self):
        pass

    def click(self):
        pass

    def hold(self):
        pass


class WindowManipulater:
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

    def screenShotForWindow(self):
        startTime = time.time()
        myTime = time.localtime(startTime)
        timeName = str(myTime.tm_mon) + "_" + str(myTime.tm_mday) + "_" + str(myTime.tm_hour) + "_" + str(
            myTime.tm_min) + "_" + str(myTime.tm_sec) + ".png"
        imgName = self.screenShotPath + timeName
        myWindow = (self.getWindowPos())
        myImg = PIL.ImageGrab.grab(bbox=myWindow,all_screens=True)
        myImg.save(imgName)
        self.logger.info("image save succeed||path=%s||spendTime=%s s",imgName,time.time()-startTime)
        return timeName


def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])

    window = WindowManipulater(Myconfig["window"]["name"],Myconfig["img"]["path"])
    photoName = window.screenShotForWindow()

if __name__ == "__main__":
    main()
