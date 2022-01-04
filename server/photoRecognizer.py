import easyocr

class PhotoRecognizer:
    def __init__(self,imgPath):
        # 创建reader对象
        self.reader = easyocr.Reader(['en','ch_sim'])
        self.imgPath = imgPath

    def recognize(self):
        result = self.reader.readtext(self.imgPath)
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