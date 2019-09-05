import cv2 as cv
import numpy as np
from PIL import Image
import os
import pytesseract
import json


def capt_process(fileDir):
    """
    对图片进行灰度化处理
    :param fileDir:是一个文件夹
    :return:
    """
    ImgList = os.listdir(fileDir)
    for Img in ImgList:
        ImgPath = os.path.join(fileDir, Img)
        text = pytesseract.image_to_string(ImgPath)
        print(text)
        """
        if len(text) != 10:
            print("Error, {}, {}".format(Img, text))
        else:
            print(text)
        """


def transfer(fileDir):
    """
    将图片转化为红色字体
    :return:
    """
    ImgList = os.listdir(fileDir)
    for img in ImgList:
        imgPath = "../Img/{}".format(img)
        image = Image.open(imgPath)
        imgArray = np.asarray(image)
        imgArray = np.require(imgArray, dtype='f4', requirements=['O', 'W'])
        print(imgArray)
        imgArray.flags.writeable = True
        imgArray[imgArray > 1] = 190
        # imgArray[imgArray == 30] = 0
        redImg = Image.fromarray(np.uint8(imgArray))

        resultParh = '../convertImg/{}'.format(img)
        redImg.save(resultParh)
        print("转化成功")


def load_numArrayDict(fileDir = '../Num/'):
    """
    加载数字数组
    :return:
    """
    NumDirList = os.listdir(fileDir)
    numArrayDict = {}
    for numDir in NumDirList:
        value = str(numDir)
        numDirPath = os.path.join(fileDir, numDir)
        try:
            numPicPath = os.listdir(numDirPath)[0]
        except IndexError:
            # 这个是All_num文件夹
            continue
        filename = os.path.join(numDirPath, numPicPath)
        NumArray = openImage(filename)
        key = str(np.sum(NumArray))
        numArrayDict[key] = value
    return numArrayDict


def openImage(filename):
    """
    读取图片转换为NumPy
    :param filename:
    :return:
    """
    image = Image.open(filename)
    imgArray = np.asarray(image)
    imgArray = np.require(imgArray, dtype='f4', requirements=['O', 'W'])
    imgArray.flags.writeable = True

    return imgArray


def write_to_json(ips):
    with open('../JsonData/num.json', 'w') as f:
        json.dump(ips, f)


def split(fileDir):
    """
    对图片进行分割
    :param fileDir:
    :return:
    """
    ImgList = os.listdir(fileDir)
    for img in ImgList:
        imgPath = "../Img/{}".format(img)
        imgArray = openImage(imgPath)
        for i in range(1, 10):
            index = i * 30
            imgs = Image.fromarray(np.uint8(imgArray[::, index - 30:index - 7, ::]))
            picName = '../Num/All_num/{}_{}.png'.format(img[:-4], i)
            imgs.save(picName)


if __name__ == "__main__":
    """
        验证码识别基本路径是灰度化,二值化,降噪,由于本此验证码无噪点,所以不用执行降噪
    """
    file_path = "../Img/"
    # transfer(file_path)
    # split(file_path)
    NumDict = load_numArrayDict()
    write_to_json(NumDict)



