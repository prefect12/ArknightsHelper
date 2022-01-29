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
        self.weekTaskElimination = 1<<10

        if not self.window.gameIsStart():
            self.startGame()

    #wating:time to sleep before press button
    #delay:time to sleep after press button
    def __clickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False
        time.sleep(waiting)
        self.mouse.move(x1 + moveX + xOffset, y1 + moveY + yOffset)
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
        self.tryToClickButton("arkNightsApp",delay=self.conf["time"]["gameStartTime"])
        self.window.getGameWindow()
        self.window.nomolizeWindowSize()
        time.sleep(self.conf["time"]["gameWatingTime"])
        self.__clickMiddleOfWindow()
        self.tryToClickButton("homePage_WatingForWeakup",delay=10)
        self.tryToClickButton("closePost")


    def checkState(self,buttonIcon):
        pass

    # skip:失败一次过后直接跳过
    def tryToClickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=3,timeOut=300,skip=False,retryGap=3):
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
            time.sleep(retryGap)
        return True


    def runOperation(self,round=10):
        if round == -1:
            round = 100000

        for i in range(round):
            self.tryToClickButton("startOperation")
            if self.tryToClickButton("takeFuckingDrug",delay=5,skip=True):
                self.tryToClickButton("startOperation")

            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("operationEnd",waiting=5,delay=5,retryGap=10)

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
        for i in range(15):
            self.tryToClickButton("visitFriendNext",skip=True)


    #返回主界面
    def navigateToHome(self):
        self.tryToClickButton("navigate",delay=5)
        self.tryToClickButton("navigateHome")

    #消费信用点数
    def buyByCridit(self):
        self.tryToClickButton("store")
        self.tryToClickButton("storeCredit")
        self.tryToClickButton("collectStoreCredit",skip=True)
        self.__clickMiddleDownOfWindow()
        for i in range(10):
            self.tryToClickButton("storeCreditItem",delay=3,skip=True)
            self.tryToClickButton("storeCreditItemBuy",delay=3,skip=True)
            self.__clickMiddleDownOfWindow()

    # 识别桌面
    def recognizeHomePage(self):
        self.logger.info("recognizeHomePage")
        newestPhotoPath = self.window.screenShotForWindow()
        results = self.recognizer.recognize(newestPhotoPath)
        for r in results:
            print(r)
        return results

    #执行每周剿灭任务全流程
    def runWeekTasks_elimination(self):
        self.gotoEliminatePage()
        self.eliminateOperation()
        self.navigateToHome()

    #执行任务
    def eliminateOperation(self):
        self.recognizeWeekTasks_eliminate()
        self.logger.info("eliminateOperation||gap = %d",self.weekTaskElimination)
        while self.weekTaskElimination != 0:
            self.tryToClickButton("startOperation")
            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("eliminateFinish",timeOut=800, waiting=10, delay=10,retryGap=10)
            self.tryToClickButton("operationEnd",waiting=10, delay=10)
            self.recognizeWeekTasks_eliminate()

    #进入剿灭界面
    def gotoEliminatePage(self):
        self.logger.info("gotoEliminatePage")
        self.tryToClickButton("terminal",waiting=3)
        self.tryToClickButton("eliminateOperation")

    #识别当前是否已经完成本周任务
    def recognizeWeekTasks_eliminate(self):
        newestPhotoPath = self.window.screenShotForWindow()
        results = self.recognizer.recognize(newestPhotoPath)
        result = [int(i) for i in [results[i+1][-2] for i in range(len(results)) if results[i][-2] == "每周报酬合成玉"][0].split("/")]
        self.weekTaskElimination = result[0] - result[1]
        self.logger.info("recognizeOperationPage||result = %d",self.weekTaskElimination)

