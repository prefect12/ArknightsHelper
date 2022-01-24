from clients import conf,log
import time
from utils import sysUtils
from server import photoSearcher,operator,photoRecognizer



class LifeCycleController:
    def __init__(self,conf):
        self.conf = conf
        self.logger = log.LoggingFactory(__name__)
        # self.recognizer = photoRecognizer.PhotoRecognizer()

    def getInfoFromHomePage(self):
        pass


    def checkCurrentStat(self):
        pass

    def move(self,curState):
        pass



def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])

    myOperator = operator.Operator(Myconfig)
    myOperator.collectFrientPoints()
    # myOperator.creditOperation()
    # myOperator.buyByCridit()
    # myOperator.navigateToHome()
    # myOperator.collectBase()
    # myOperator.collectTaskItem()
    # myOperator.runOperation()

    # myOperator.navigateToHome()
    



def testFunc():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])
    # myrecognizer = photoRecognizer.PhotoRecognizer(Myconfig["img"]["screenShotsPath"]+"homePage_WatingForWeakup.png")
    # myrecognizer.recognize()
    # myrecognizer
    result = photoSearcher.findPosition("./images/ScreenShots/1_19_0_17_24.png","./images/OperationIcon/friendFriendList.png")

    # window = windowManipulator.WindowManipulator(Myconfig["initWindowConfig"],Myconfig["img"]["screenShotsPath"])
    # window.nomolizeWindowSize()

if __name__ == "__main__":
    main()
    # testFunc()