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
        self.window = windowManipulator.WindowManipulator(myConfig["initWindowConfig"],myConfig["img"]["screenShotsPath"])
        self.newestPhotoPath = ""
        self.startGame()


    def run(self):
        while True:
            if time.localtime(time.time()).tm_min % 3 == 0:
                sysUtils.clearScreenShots()
            self.waitingClickButton("startOperation")
            self.waitingClickButton("startOperationInOperatorView")
            self.waitingClickButton("operationEnd",timeWait=5)

    def waitingClickButton(self,buttonIcon,timeWait=0):
        while True:
            result = self.clickButton(buttonIcon,timeWait)
            if result == True:
                self.logger.info("current Operation: Operation Truly End",)
                break
            time.sleep(5)
        return True

    def checkState(self):
        x,y = photoSearcher.findPosition(self.newestPhotoPath, self.buttons["startOperation"])
        if x != -1 and y != -1:
            self.currentState = 0

        x,y = photoSearcher.findPosition(self.newestPhotoPath, self.buttons["startOperationInOperatorView"])
        if x != -1 and y != -1:
            self.currentState = 1

        x,y = photoSearcher.findPosition(self.newestPhotoPath, self.buttons["operationEnd"])
        if x != -1 and y != -1:
            self.currentState = 2

        x,y = photoSearcher.findPosition(self.newestPhotoPath, self.buttons["uploadingData"])
        if x != -1 and y != -1:
            self.currentState = -1

    def clickButton(self,buttonIcon,timeWait=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False
        self.mouse.move(x1 + moveX, y1 + moveY)
        time.sleep(timeWait)
        self.mouse.leftClick()
        time.sleep(1)
        return True

    def startGame(self):
        self.waitingClickButton("arkNightsApp")
        self.window.getGameWindow()

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
    myOperator.run()
    # myOperator.startGame()
    # myControl.run()
    # sysUtils.clearScreenShots()

def testFunc():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])
    # myrecognizer = photoRecognizer.PhotoRecognizer(Myconfig["img"]["screenShotsPath"]+"1.png")
    # myrecognizer.recognize()
    # myrecognizer
    result = photoSearcher.findPosition("./images/ScreenShots/1_5_23_30_26.png","./images/OperationIcon/arkNightsApp.png")

    # window = windowManipulator.WindowManipulator(Myconfig["initWindowConfig"],Myconfig["img"]["screenShotsPath"])
    # window.nomolizeWindowSize()

if __name__ == "__main__":
    main()
    # testFunc()