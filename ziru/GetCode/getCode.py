import requests
import time
import re
from queue import Queue
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': ua.random}


def getCon(url):
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        else:
            print("连接失败:{}".format(resp.status_code))
            return 0
    except Exception as e:
        print("Error {} ,{}".format(url, e))
        pass


def parse(text, imgQueue):
    imgUrl = re.search(r'<span class="num" style="background-image: url(.*?);background-position: (.*?)"></span>', text)
    price_num = int((-1 * float(imgUrl.group(2)[:-2]) / 21.4))  # 获取数字所在位置,位置是以21.4px间隔
    imgUrl = 'http:' + re.sub(r'\(|\)', '', imgUrl.group(1))
    imgQueue.put((imgUrl, price_num))
    return imgQueue
    """for i in imgUrl:
        price_num = int((-1*float(i[-1][:-2])/21.4))  # 获取数字所在位置
        imgUrl = 'http:'+re.sub(r'\(|\)', '', i[0])
        if imgUrl not in imgUrls:
            imgUrls.append(imgUrl)
            imgQueue.put((imgUrl, price_num))
    return imgQueue
    """


def getImg(ImageCodes, imgQueue):
    while not imgQueue.empty():
        ImageCode = imgQueue.get()
        imgUrl = ImageCode[0]
        imgCode = ImageCode[-1]
        ImgName = str(time.time())[-4:] + '_' + str(imgCode)
        ImgPath = '../Img/{}.png'.format(ImgName)
        resp = requests.get(imgUrl, headers=headers)
        with open(ImgPath, 'wb') as f:
            f.write(resp.content)
        print('成功获取')


def main():
    base_url = 'http://sz.ziroom.com/z/p{}/'
    imgQueue = Queue()
    for i in range(100):
        final_url = base_url.format(str(i))
        print(final_url)
        text = getCon(final_url)
        ImageCodes = parse(text, imgQueue)
        getImg(ImageCodes, imgQueue)


"""
if __name__ == "__main__":
    base_url = 'http://sz.ziroom.com/z/p{}/'
    imgQueue = Queue()
    for i in range(100):
        final_url = base_url.format(str(i))
        print(final_url)
        text = getCon(final_url)
        ImageCodes = parse(text, imgQueue)
        getImg(ImageCodes, imgQueue)
"""