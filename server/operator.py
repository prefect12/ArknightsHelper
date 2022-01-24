from clients import conf,log
from server import mouseController,windowManipulator,photoRecognizer,photoSearcher
import time



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
    def run(self,timeOut=300,failAwait=5):
        i = 0
        startTime = time.time()
        while i < len(self.workingQueue):
            if self.workingQueue[i]():
                i += 1
            else:
                time.sleep(failAwait)
                if i > 1:
                    i -= 1
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

    def __clickMiddleDownOfWindow(self,delay=0):
        x1, y1, x2, y2 = self.window.getWindowPos()
        self.mouse.move((x1 + x2) / 2, (y1 + y2) * 2 / 3)
        self.mouse.leftClick()
        time.sleep(delay)

    def startGame(self):
        self.__clickButton("arkNightsApp",self.conf["time"]["gameStartTime"])
        self.window.getGameWindow()
        self.window.nomolizeWindowSize()
        time.sleep(self.conf["time"]["gameWatingTime"])
        self.__clickMiddleOfWindow(5)
        self.__clickButton("homePage_WatingForWeakup",10)
        self.__clickButton("closePost")

    def checkState(self,buttonIcon):
        pass

    # skip:失败一次过后直接跳过
    def tryToClickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=3,timeOut=600,skip=False):
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
            self.tryToClickButton("startOperation")
            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("operationEnd",waiting=10,delay=10)

    #collection items from base
    #基建收菜
    def collectBase(self):
        self.tryToClickButton("base",skip=True)
        self.tryToClickButton("baseRing",waiting=5)
        for i in range(3):
            self.tryToClickButton("baseTodoList",xOffset=100,skip=True)
        self.navigateToHome()

    #daily task collection
    #任务收菜
    def collectTaskItem(self):
        self.tryToClickButton("task",skip=True)
        self.tryToClickButton("taskCollectAll",skip=True)
        self.__clickMiddleDownOfWindow()
        self.navigateToHome()

    #信用点数全流程
    def creditOperation(self):
        self.collectFrientPoints()
        self.navigateToHome()
        self.buyByCridit()
        self.navigateToHome()

    # 收集信用点数
    def collectFrientPoints(self):
        self.tryToClickButton("friendPage")
        self.tryToClickButton("friendList")
        self.tryToClickButton("visitFriend")
        for i in range(10):
            self.tryToClickButton("visitFriendNext")
        # self.addJob(self.warp(self.tryToClickButton,"friendPage"))
        # self.addJob(self.warp(self.tryToClickButton, "friendList"))
        # self.addJob(self.warp(self.tryToClickButton, "visitFriend"))
    #返回主界面
    def navigateToHome(self):
        self.tryToClickButton("navigate")
        self.tryToClickButton("navigateHome")

    #消费信用点数
    def buyByCridit(self):
        self.tryToClickButton("store")
        self.tryToClickButton("storeCredit",skip=True)
        self.tryToClickButton("collectStoreCredit",skip=True)
        self.__clickMiddleDownOfWindow()
        for i in range(10):
            self.tryToClickButton("storeCreditItem",delay=1,skip=True)
            self.tryToClickButton("storeCreditItemBuy",delay=1,skip=True)
            self.__clickMiddleDownOfWindow()

    def recognizeHomePage(self):
        self.logger.info("recognizeHomePage")
        newestPhotoPath = self.window.screenShotForWindow()
        self.recognizer.recognize(newestPhotoPath)

    def warp(self,func,args):
        def myFunc(func,args):
            return func(args)
        return myFunc
