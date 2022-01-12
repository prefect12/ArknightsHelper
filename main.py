from clients import conf,log
import time
from utils import sysUtils
from server import mouseController,windowManipulator,photoRecognizer,photoSearcher


# startOperation="./images/items/startOperation.png"
# startOperationInOperatorView="./images/items/starOperationInOperatorView.png"
# operationEnd="./images/items/operationEnd.png"

class Operator:
    def __init__(self,myConfig):
        self.conf = myConfig
        self.logger = log.LoggingFactory.logger(__name__)
        self.buttons = myConfig["buttons"]
        self.mouse = mouseController.MouseController()
        self.window = windowManipulator.WindowManipulator(self.conf["initWindowConfig"],self.conf["img"])
        self.newestPhotoPath = ""
        if not self.window.gameIsStart():
            self.startGame()

    #delay:time to sleep after press button
    def __clickButton(self,buttonIcon,waiting=0,delay=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False
        self.mouse.move(x1 + moveX, y1 + moveY)
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
    # timeOut:超时时间，设置了超时时间则skip设置为False，两个参数互斥
    def tryToClickButton(self,buttonIcon,waiting=0,delay=5,timeOut=600,skip=False):
        result = False
        startTime = time.time()
        while result != True:
            result = self.__clickButton(buttonIcon,waiting,delay)
            time.sleep(5)
            if time.time() - startTime > timeOut:
                self.logger.error("click button timeout!!! %s",buttonIcon)
                return False
            if skip == True:
                self.logger.info("click button skip!!! %s",buttonIcon)
                return result
        return True


    def runOperation(self):
        for i in range(50):
            self.tryToClickButton("startOperation")
            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("operationEnd",waiting=10,delay=10)



class LifeCycleController:
    def __init__(self):
        pass

    def checkCurrentStat(self):
        pass

    def move(self,curState):
        pass



def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])

    myOperator = Operator(Myconfig)
    myOperator.runOperation()
    



def testFunc():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])
    # myrecognizer = photoRecognizer.PhotoRecognizer(Myconfig["img"]["screenShotsPath"]+"homePage_WatingForWeakup.png")
    # myrecognizer.recognize()
    # myrecognizer
    result = photoSearcher.findPosition("./images/ScreenShots/1_7_0_55_16.png","./images/OperationIcon/arkNightsApp.png")

    # window = windowManipulator.WindowManipulator(Myconfig["initWindowConfig"],Myconfig["img"]["screenShotsPath"])
    # window.nomolizeWindowSize()

if __name__ == "__main__":
    main()
    # testFunc()