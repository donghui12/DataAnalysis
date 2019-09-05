# 该文件夹是对验证码进行操作
IdentifyingCode.py 是主要识别验证码的文件
Test.py 是测试文件
images 是测试时的文件夹图片所在地址
NumPic 是测试时分割验证码的地址

具体思路：
    由于自如的验证码除了顺序不一样,其他都一样,
    所以我们只需要识别一个验证码,然后保存不同数字
    将不同数字图片转换为NumPy.Array,然后np.sum()求和
    经测试,每个数字的和不一样,返回一个dict.
    {'数组和':'数字'}
    
该程序只适用于自如,其他网站还需要进行识别验证码（需要用到深度学习）

IdentifyingCode.py

    transfer(fileDir):
        传入一个验证码所在文件夹位置路径,
        将图片上的字转换成其他颜色,
        在本程序中没用
        
    capt_process(fileDir):
        传入一个验证码所在文件夹位置路径,
        然后查看文件夹下图片名称
        然后尝试使用OCR识别,在本程序中没用到
        
    split(fileDir):
        然后对图片进行切割,切割结果存到返回一个'../Num/All_num/'
        然后需要自己将All_num中的图片分到每个文件夹里
    
    
    load_numArrayDict(fileDir = '../Num/'):
        传入一个分割后的验证码文件夹
        返回一个numArrayDict
        
    openImage(filename):
        读取图片转换为NumPy
    
    write_to_json(dict):
        将dict写入到json文件里,
        文件路径在‘../JsonData/num.json’