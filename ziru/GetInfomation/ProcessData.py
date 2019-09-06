import requests
from ziru.GetCode.getCode import headers
from ziru.CodeDemo import IdentifyingCode
import json
from PIL import Image
import numpy as np


def loadData(filename):
    """
    加载信息
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        data = f.read()
    DATA = json.loads(data)
    return DATA


def saveData(CodeDict, filename):
    CodeJson = json.dumps(CodeDict)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(CodeJson)


def processPageCode(pageCode):
    """
    处理pageNum文件
    :param pageCode:
    :return:
    """
    CodeDict = {}
    for info in pageCode:
        print(info)
        for pageNum, codeUrl in info.items():
            CodeUrl = 'http:'+codeUrl[1:-1]
            code = processCode(CodeUrl)
            CodeDict[pageNum] = code
    saveData(CodeDict, 'pageNumCode.json')
    return CodeDict


def processCode(codeUrl):
    """
    类似于OCR,传入一个验证码URL,返回该验证码识别结果
    :param codeUrl:
    :return:
    """
    img = requests.get(codeUrl, headers=headers).content
    with open('Code.png', 'wb') as f:
        f.write(img)
    CodeImgArray = IdentifyingCode.openImage('Code.png')

    Code = []
    for i in range(1, 11):
        index = i * 30
        imgs = Image.fromarray(np.uint8(CodeImgArray[::, index - 30:index - 7, ::]))
        Code.append(numCode[str(np.sum(imgs))+'.0'])
    return ''.join(Code)


def processRoomData(roomData):
    """
    通过room中的price_location,得知价格数字在验证码的位置
    然后通过验证码和pageNum的对应找到房间对应的验证码,然后获取价格
    :param roomData:
    :return:
    """
    resultRoomData = []
    for room in roomData:
        price = []
        for i in room['price_location']:
            print(int(i)+1)
            print(CodeNum[str(room['pageNum'])])
            price.append(CodeNum[str(room['pageNum'])][int(i)+1])
        if int(''.join(price)) < 1500:
            ''.join(price).replace('3', '9')
        room['price'] = ''.join(price)
        resultRoomData.append(room)
    return resultRoomData


if __name__=="__main__":
    """
    这一部分是对{pageNum:CodeUrl } 进行处理, 识别CodeUrl的验证码顺序
    返回一个dict类型 {'1':验证码1, '2': 验证码2, ...}
    numCode = loadData('../JsonData/num.json')
    pageNum = loadData('pageNum.json')
    processPageCode(pageNum) 
    """

    # 这一部分是对roomData进行处理, 添加price 进room中的
    # 具体方法看代码
    CodeNum = loadData('pageNumCode.json')
    roomData = loadData('resultData.json')
    resultRoomData = processRoomData(roomData)
    saveData(resultRoomData, 'resultRoomDataJson.json')


