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
        从Queue中获取信息
        执行parseRoomPage函数
       
    parseRoomPage(room_html, roomUid):
        从该页面获取信息
        使用lxml和re结合
        返回一个字典类型
    
    该文件执行顺序:
    GetRoomUrl --> GetInformation
        