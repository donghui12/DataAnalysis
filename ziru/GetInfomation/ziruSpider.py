import re
from ziru.GetCode import getCode
from queue import Queue
from lxml import etree
import json

PageNumPic = []  # 用来存储每个页面对应验证码网址
result = []  # 用来存储每个room信息


def GetRoomUrl(html, pageNum):
    """
    获取具体房子uid,并加入到roomUidQueue中
    :param html:
    :return:
    """
    pic = re.search('<span class="num" style="background-image: url(.*?);background-position:.*?px"></span>', html)
    # print(pic.group(1))

    PageNumPicDict = {pageNum: pic.group(1)}
    PageNumPic.append(PageNumPicDict)

    page = etree.HTML(html)
    item = page.xpath('//div[@class="item"]')
    for i in item:
        try:
            link = i.xpath('./div[@class="pic-box"]/a/@href')[0]
        except IndexError as e:
            continue
        price_pic = i.xpath('./div[@class="info-box"]/div[@class="price"]/span/@style')
        position = []
        for j in price_pic:
            a = re.search('background-position: (.*?)px', j).group(1)
            position.append(str(-1 * int(float(a) / 22.4)))
        roomUidQueue.put((pageNum, link, ''.join(position)))


def GetInformation():
    """
    获取主要信息
    :return:
    """
    while not roomUidQueue.empty():
        roomUid = roomUidQueue.get()
        roomPageURL = 'http:' + roomUid[1]
        pageText = getCode.getCon(roomPageURL)
        try:
            roomDict = parseRoomPage(pageText, roomUid)
            result.append(roomDict)
            print("获取成功")
        except IndexError as e:
            print(e)
            continue


def parseRoomPage(room_html, roomUid):
    roomPage = etree.HTML(room_html)

    room_area = roomPage.xpath('//div[@class="Z_home_info"]/div[1]/dl[1]/dd[1]/text()')[0].replace('㎡', '')  # 房屋使用面积
    # print('room_area:{}'.format(room_area))

    room_type = roomPage.xpath('//div[@class="Z_home_info"]/div[1]/dl[3]/dd[1]/text()')[0]  # 房屋类型 类似于：4室1厅
    # print('room_type:{}'.format(room_type))
    room_num, Parlor_num = room_type[0], room_type[-2]  # 房屋数量 , 客厅数量
    # print('room_num:{}\nParlor_num:{}'.format(room_num, Parlor_num))

    location = roomPage.xpath('//span[@class="ad"]/text()')[0]  # 位置描述
    # print(location)
    if len(re.findall(r'[\d]+', location)) is 2:
        subway_line, distance_to_subway = re.findall(r'[\d]+', location)  # 地铁线路
    else:
        print('地址错误')
    # print('地铁线路:{}\n距离地铁站：{}'.format(subway_line, distance_to_subway))

    floor_num = eval(roomPage.xpath('//ul[@class="Z_home_o"]/li[2]/span[@class="va"]/text()')[0])  # 获取楼层
    # print('楼层:{}'.format(floor_num))

    lift_info = roomPage.xpath('//div[@class="Z_home_o"]/li[3]/span[@class="va"]/text()')  # 获取楼层
    lift = 0  # 获取电梯, 默认没有电梯
    if lift_info == '有':
        lift = 1

    furniture_num = roomPage.xpath('//div[@class="Z_info_icons "]/dl/dt/text()')  # 获取家具数量
    # print(furniture_num)
    # print('家具数量:{}'.format(len(furniture_num)))

    if '空调' in furniture_num or '中央空调' in furniture_num:
        Air_Conditioning = 1
    else:
        Air_Conditioning = 0
    # print("空调数量: {}".format(Air_Conditioning))

    if '冰箱' in furniture_num:
        refrigerator = 1
    else:
        refrigerator = 0
    # print("冰箱数量: {}".format(refrigerator))

    if '热水器' in furniture_num:
        HotWater = 1
    else:
        HotWater = 0
    # print("热水器数量: {}".format(HotWater))

    pageNum = roomUid[0]
    price_location = roomUid[-1]

    roomDict = {
        'room_area': room_area,
        'room_num': room_num,
        'Parlor_num': Parlor_num,
        'subway_line': subway_line,
        'distance_to_subway': distance_to_subway,
        'floor_num': floor_num,
        'lift': lift,
        'refrigerator': refrigerator,
        'HotWater': HotWater,
        'furniture_num': len(furniture_num),
        'pageNum': pageNum,
        'price_location': price_location
    }
    return roomDict


if __name__ == '__main__':
    roomUidQueue = Queue()  # 该队列存储RoomUid,且不重复

    base_url = 'http://sz.ziroom.com/z/p{}/'  # 这个是基本的页面URL
    Test_url = 'http://sz.ziroom.com/z/p1/'

    BaseRoomURL = 'http://sz.ziroom.com/x/{}.html'  # 这个是某个租房详情页面
    TestRoomURL = 'http://sz.ziroom.com/x/741141968.html'

    for i in range(1, 100):
        try:
            final_url = base_url.format(i)
            text = getCode.getCon(Test_url)
            GetRoomUrl(text, i)
            GetInformation()
        except Exception as e:
            continue

    resultData = json.dumps(result)
    with open('resultData.json', 'w', encoding='utf-8') as f:
        f.write(resultData)

    PageNumPicJson = json.dumps(PageNumPic)
    with open('pageNum.json', 'w', encoding='utf-8') as f:
        f.write(PageNumPicJson)
    # parseRoomPage(text, 2)
