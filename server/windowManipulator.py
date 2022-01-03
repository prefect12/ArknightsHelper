import time
from PIL import ImageGrab
from clients import log
import win32gui


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
        myImg = ImageGrab.grab(bbox=(self.getWindowPos()),all_screens=True)
        myImg.save(imgName)
        self.logger.info("image save succeed||path=%s||spendTime=%sSecond",imgName,time.time()-startTime)
        return imgName
