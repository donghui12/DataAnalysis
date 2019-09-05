import numpy as np
from PIL import Image
imgPath = '../Num/0/0036_5_4.png'
imgPath2 = '../Num/0/0042_8_4.png'

image = Image.open(imgPath)
imgArray = np.asarray(image)
imgArray = np.require(imgArray, dtype='f4', requirements=['O', 'W'])
imgArray.flags.writeable = True

image2 = Image.open(imgPath2)
imgArray2 = np.asarray(image2)
imgArray2 = np.require(imgArray2, dtype='f4', requirements=['O', 'W'])
imgArray2.flags.writeable = True

print(sum(imgArray) == sum(imgArray2))

"""

# all_zero_in_row = np.array([np.all(row == 0.) for row in imgArray])
any_zero_in_row = np.array([print(sum(row)) for row in imgArray])

imgArray[any_zero_in_row] = 1
imgArray[imgArray == 0] = 255
imgArray[any_zero_in_row] = 0


print(imgArray)

imgs =  Image.fromarray(np.uint8(imgArray))
picName = 'Test.png'
imgs.save(picName)
"""
"""

for i in range(1, 10):
    index = i*30
    imgs =  Image.fromarray(np.uint8(imgArray[::, index-30:index-7, ::]))
    picName = './NumPic/{}.png'.format(i)
    imgs.save(picName)
"""