import time
from PIL import ImageGrab
from clients import log
import win32gui
import os


class WindowManipulator:
    def __init__(self,initWindowConfig,screenShotPath):
        self.logger = log.LoggingFactory.logger(__name__)
        self.config = initWindowConfig
        self.screenShotPath = screenShotPath
        self.startEmulator(self.config["retry"])

    def getGameWindow(self):
        self.handle = win32gui.FindWindow(0,self.config["emulatorGameName"])

    def startEmulator(self,retry):
        os.system(self.config["emulatorPath"])
        time.sleep(self.config["emulatorStartTime"])
        self.logger("Start Emulator || try to get window...")
        self.isEmulatorStart(retry-1)

    def isEmulatorStart(self,retry):
        if retry == 0:
            return False
        self.handle = win32gui.FindWindow(0, self.config["emulatorName"])
        if self.handle == 0:
            self.logger.info("Can't find screen... || try to start emulator || number of retry%d",retry)
            return self.startEmulator(retry)
        self.logger.info("Get Emulator window success!!")
        return True

    def setWindowForeground(self):
        win32gui.SetForegroundWindow(self.handle)

    def getWindowPos(self):
        return  win32gui.GetWindowRect(self.handle)

    def getWindowLeftUpCornerPos(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.handle)
        return x1,y1

    def getWindowRightDownCornerPos(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.handle)
        return x2,y2

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
