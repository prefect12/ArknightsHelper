from clients import conf,log
import time
import easyocr
from utils import photoUtils,sysUtils
from server import mouseController,windowManipulator


# startOperation="./images/items/startOperation.png"
# startOperationInOperatorView="./images/items/starOperationInOperatorView.png"
# operationEnd="./images/items/operationEnd.png"

class Controller:
    def __init__(self,myConfig):
        self.currentState = 0
        self.window = windowManipulator.WindowManipulator(myConfig["window"]["name"],myConfig["img"]["path"])
        self.mouse = mouseController.MouseController()
        self.newestPhotoPath = ""
        self.logger = log.LoggingFactory.logger(__name__)
        self.buttons = myConfig["buttons"]

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
        x,y = photoUtils.findPosition(self.newestPhotoPath, self.buttons["startOperation"])
        if x != -1 and y != -1:
            self.currentState = 0

        x,y = photoUtils.findPosition(self.newestPhotoPath, self.buttons["startOperationInOperatorView"])
        if x != -1 and y != -1:
            self.currentState = 1

        x,y = photoUtils.findPosition(self.newestPhotoPath, self.buttons["operationEnd"])
        if x != -1 and y != -1:
            self.currentState = 2

        x,y = photoUtils.findPosition(self.newestPhotoPath, self.buttons["uploadingData"])
        if x != -1 and y != -1:
            self.currentState = -1

    def clickButton(self,buttonIcon,timeWait=0):
        buttonIconPath = self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoUtils.findPosition(self.newestPhotoPath, buttonIconPath)
        x1, y1 = self.window.getWindowLeftUpCornerPos()
        if moveX == -1 and moveY == -1:
            return False
        self.mouse.move(x1 + moveX, y1 + moveY)
        time.sleep(timeWait)
        self.mouse.leftClick()
        time.sleep(1)
        return True

def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])
    myControl = Controller(Myconfig)
    myControl.run()
    # sysUtils.clearScreenShots()

if __name__ == "__main__":
    main()
