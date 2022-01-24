import easyocr

class PhotoRecognizer:
    def __init__(self):
        # 创建reader对象
        self.reader = easyocr.Reader(['ch_sim'])


    def recognize(self,imgPath):
        result = self.reader.readtext(imgPath)
        for i in result:
            print(i)

    def recognizeItemNum(self):
        pass

    #return number of item
    def recognizeNum(self):
        pass

    #return location of a level
    def recognizeLevel(self):
        pass

