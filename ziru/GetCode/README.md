# getCode.py是用来获取验证码图片
parse(text, imgQueue) 解析获取的responce.text文件,然后使用re正则表达式获取图片url和相对位置
然后进行解析,生成一个元组(url,position),将元组插入Queue中
getImg(ImageCodes, imgQueue) 获取图片,从Queue中获取元组,然后下载图片,命名规则是time.time()[-4:]+"_"+positon+'.png'
保存下载