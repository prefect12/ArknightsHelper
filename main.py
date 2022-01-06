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
        self.startGame()



    def __clickButton(self,buttonIcon,delay=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False
        self.mouse.move(x1 + moveX, y1 + moveY)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    def __clickMiddleOfWindow(self,delay=0):
        x1,y1,x2,y2 = self.window.getWindowPos()
        self.mouse.move((x1+x2)/2,(y1+y2)/2)
        self.mouse.leftClick()
        time.sleep(5)

    def startGame(self):
        self.__clickButton("arkNightsApp",self.conf["time"]["gameStartTime"])
        self.window.getGameWindow()
        self.window.nomolizeWindowSize()
        time.sleep(self.conf["time"]["gameWatingTime"])
        self.__clickMiddleOfWindow(5)
        self.__clickButton("homePage_WatingForWeakup",10)


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