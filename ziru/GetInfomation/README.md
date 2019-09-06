# 该文件夹主要是进行数据抓取
# pageNum.json是抓取的文件,里边是房间信息
# resultData.json 是页面对应本页面的验证码URL
# setQueue.py 本来是为了消除重复URL, 但是没办法插入元组,就没用到
# ziruSpider.py:
    
    GetRoomUrl(html, pageNum):
        html:主页面text,http://sz.ziroom.com/z/p1/ 的信息
        pageNum: 是该页面的页面数
        获取该页面中的 roomPageUrl (房间具体链接)和该页面的验证码url
        并组成元组(pageNum, roomPageUrl, capUrl)
        加入到Queue()中
        
    GetInformation():
        主要运行文件
        从Queue中p获取信息
        执行parseRoomPage函数
       
    parseRoomPage(room_html, roomUid):
        从该页面获取信息
        使用lxml和re结合
        返回一个字典类型
    
    该文件执行顺序:
    GetRoomUrl --> GetInformation
# ProcessData.py:
    对数据进行基本处理
    processRoomData(roomData):
        通过room中的price_location,得知价格数字在验证码的位置
        然后通过验证码和pageNum的对应找到房间对应的验证码,然后获取价格
    
    processCode(codeUrl):
        类似于OCR,传入一个验证码URL,返回该验证码识别结果
        CodeUrl_1 --> CodeNum_1
        
    processPageCode(pageCode):
        处理pageNum文件
        从[ {pageNum_1: CodeUrl_1},{pageNum_2: CodeUrl_2},{pageNum_3: CodeUrl_3},...]
        变成{pageNum_1: CodeNum_1,pageNum_2: CodeNum_2,pageNum_3: CodeNum_3,...}    
        