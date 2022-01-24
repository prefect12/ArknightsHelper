from clients import conf,log
from server import mouseController,windowManipulator,photoRecognizer,photoSearcher
import time
from functools import wraps



class Operator:
    def __init__(self,myConfig):
        self.conf = myConfig
        self.logger = log.LoggingFactory.logger(__name__)
        self.buttons = myConfig["buttons"]
        self.mouse = mouseController.MouseController()
        self.window = windowManipulator.WindowManipulator(self.conf["initWindowConfig"],self.conf["img"])
        self.recognizer = photoRecognizer.PhotoRecognizer()
        self.workingQueue = []
        self.newestPhotoPath = ""

        if not self.window.gameIsStart():
            self.startGame()

    # 执行函数队列
    def run(self,funcName,timeOut=300,failAwait=5,retry=2):
        self.logger.info("working queue is running||functionName=%s||workingQueue=%s",funcName,self.workingQueue)
        i = 0
        startTime = time.time()
        while i < len(self.workingQueue):
            print(i)
            if self.workingQueue[i]():
                i += 1
            else:
                time.sleep(failAwait)
                if i > 1 and retry > 0 and self.workingQueue[i-1]() == False:
                    retry -= 1
                if time.time() - startTime > timeOut:
                    self.workingQueue = []
                    return False
        self.workingQueue = []
        return True

    def addJob(self,job):
        self.workingQueue.append(job)

    #delay:time to sleep after press button
    #wating:time to sleep before press button

    def __clickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False
        self.mouse.move(x1 + moveX + xOffset, y1 + moveY + yOffset)
        time.sleep(waiting)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    # delay:time to sleep after press button
    def __clickMiddleOfWindow(self,delay=0):
        x1,y1,x2,y2 = self.window.getWindowPos()
        self.mouse.move((x1+x2)/2,(y1+y2)/2)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    def __clickMiddleDownOfWindow(self,delay=0):
        x1, y1, x2, y2 = self.window.getWindowPos()
        self.mouse.move((x1 + x2) / 2, (y1 + y2) * 2 / 3)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    def startGame(self):
        self.addJob(warpTryClick(self.tryToClickButton,"arkNightsApp",waiting=self.conf["time"]["gameStartTime"]))
        self.addJob(self.window.getGameWindow)
        self.addJob(self.window.nomolizeWindowSize)
        self.addJob(warSleep(self.conf["time"]["gameWatingTime"]))
        self.addJob(self.__clickMiddleOfWindow)
        self.addJob(warpTryClick(self.tryToClickButton,"homePage_WatingForWeakup",delay=10))
        self.addJob(warpTryClick(self.tryToClickButton,"closePost"))
        self.run("startGame")

    def checkState(self,buttonIcon):
        pass

    # skip:失败一次过后直接跳过
    def tryToClickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=3,timeOut=300,skip=False):
        result = False
        startTime = time.time()
        while result != True:
            result = self.__clickButton(buttonIcon,xOffset,yOffset,waiting,delay)
            if time.time() - startTime > timeOut:
                self.logger.error("click button timeout!!! %s",buttonIcon)
                return False
            if skip == True:
                self.logger.info("click button skip!!! %s",buttonIcon)
                return result
        return True


    def runOperation(self,round=10):
        for i in range(round):
            self.addJob(warpTryClick(self.tryToClickButton,"startOperation"))
            self.addJob(warpTryClick(self.tryToClickButton,"startOperationInOperatorView"))
            self.addJob(warpTryClick(self.tryToClickButton,"operationEnd",waiting=10,delay=10))

    #collection items from base
    #基建收菜
    def collectBase(self):
        self.addJob(warpTryClick(self.tryToClickButton,"base",skip=True))
        self.addJob(warpTryClick(self.tryToClickButton,"baseRing",waiting=5))
        for i in range(3):
            self.addJob(warpTryClick(self.tryToClickButton,"baseTodoList",xOffset=100,skip=True))
        self.navigateToHome()

    #daily task collection
    #任务收菜
    def collectTaskItem(self):
        self.addJob(warpTryClick(self.tryToClickButton,"task",skip=True))
        self.addJob(warpTryClick(self.tryToClickButton,"taskCollectAll",skip=True))
        self.addJob(self.__clickMiddleDownOfWindow)
        self.navigateToHome()

    #信用点数全流程
    def creditOperation(self):
        self.collectFrientPoints()
        self.navigateToHome()
        self.buyByCridit()
        self.navigateToHome()

    # 收集信用点数
    def collectFrientPoints(self):
        self.addJob(warpTryClick(self.tryToClickButton,"friendPage"))
        self.addJob(warpTryClick(self.tryToClickButton, "friendList"))
        self.addJob(warpTryClick(self.tryToClickButton, "visitFriend"))

        for i in range(10):
            self.addJob(warpTryClick(self.tryToClickButton, "visitFriendNext"))
        self.run("collectFrientPoints")

    #返回主界面
    def navigateToHome(self):
        self.addJob(warpTryClick(self.tryToClickButton,"navigate",delay=5))
        self.addJob(warpTryClick(self.tryToClickButton,"navigateHome"))

    #消费信用点数
    def buyByCridit(self):
        self.addJob(warpTryClick(self.tryToClickButton,"store"))
        self.addJob(warpTryClick(self.tryToClickButton,"storeCredit"))
        self.addJob(warpTryClick(self.tryToClickButton,"collectStoreCredit",skip=True))
        self.addJob(self.__clickMiddleDownOfWindow)
        for i in range(10):
            self.addJob(warpTryClick(self.tryToClickButton,"storeCreditItem",delay=1,skip=True))
            self.addJob(warpTryClick(self.tryToClickButton,"storeCreditItemBuy",delay=1,skip=True))
            self.addJob(self.__clickMiddleDownOfWindow)

    def recognizeHomePage(self):
        self.logger.info("recognizeHomePage")
        newestPhotoPath = self.window.screenShotForWindow()
        self.recognizer.recognize(newestPhotoPath)


def warpTryClick(func,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=3,timeOut=300,skip=False):
    def myFunc():
        return func(buttonIcon,xOffset,yOffset,waiting,delay,timeOut,skip)
    return myFunc

def warSleep(mytime):
    def myFunc():
        time.sleep(mytime)
        return True
    return myFunc