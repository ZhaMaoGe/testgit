# -*- coding:utf8 -*-
from PIL import Image,ImageFont,ImageDraw,ImageFilter
import random
#返回随机字母

def charRandom():
	return chr((random.randint(65,90)))
#返回随机数字
def numRandom():
	return random.randint(0,9)
#随机颜色
def colorRandom1():
	return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
#随机长生颜色2
def colorRandom2():
	return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
def photo_create():
	width = 25*4
	height = 34
	image = Image.new('RGB', (width,height), (255,255,255));
	#创建font对象
	font = ImageFont.truetype('C:\\windows\Fonts\Arial.ttf',24);
	#创建draw对象
	draw = ImageDraw.Draw(image)
	#填充每一个颜色
	# x=0
	# y=0
	# while x < width:
	# 	while y < height:
	# 		y=y+2
	# 		x=x+2
	for x in range(0, width, 2):
		for y in range(0, height, 2):
			draw.point((x,y), fill=colorRandom1())

	randomstr = ""
	for i in range(4):
		randomstr += charRandom()
	# randomstr=charRandom()
	#输出文字
	for t, ch in enumerate(randomstr):
		draw.text((25*t+10,10), ch, font=font, fill=colorRandom2())
	#模糊
	image = image.filter(ImageFilter.BLUR)
	image.save('demo/static/demo/images/code.jpg','jpeg')
	return randomstr
