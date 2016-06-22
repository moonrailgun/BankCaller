#coding:utf-8

import RPi.GPIO as GPIO
import spidev
import time

Max7219_pinCS = 24
Button_inputPin = 20
Button_VCCPin = 21

numList = [
[0x3C,0x42,0x42,0x42,0x42,0x42,0x42,0x3C],# 0
[0x10,0x30,0x50,0x10,0x10,0x10,0x10,0x7C],# 1
[0x3E,0x02,0x02,0x3E,0x20,0x20,0x3E,0x00],# 2
[0x00,0x7C,0x04,0x04,0x7C,0x04,0x04,0x7C],# 3
[0x08,0x18,0x28,0x48,0xFE,0x08,0x08,0x08],# 4
[0x3C,0x20,0x20,0x3C,0x04,0x04,0x3C,0x00],# 5
[0x3C,0x20,0x20,0x3C,0x24,0x24,0x3C,0x00],# 6
[0x3E,0x22,0x04,0x08,0x08,0x08,0x08,0x08],# 7
[0x00,0x3E,0x22,0x22,0x3E,0x22,0x22,0x3E],# 8
[0x3E,0x22,0x22,0x3E,0x02,0x02,0x02,0x3E],# 9
]
full = [0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
clear = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

spi = spidev.SpiDev()
spi.open(0,0)#bus, device
spi.mode = 0

def writeByte(_data):
	GPIO.output(Max7219_pinCS, GPIO.LOW) # 输出低电平
	#spi.xfer(_data)
	spi.writebytes(_data)
	GPIO.output(Max7219_pinCS, GPIO.HIGH) # 输出高电平

# 初始化MAX7219模块
def initMAX7219():
	writeByte([0x09,0x00,0x09,0x00])
	writeByte([0x0a,0x03,0x0a,0x03])
	writeByte([0x0b,0x07,0x0b,0x07])
	writeByte([0x0c,0x01,0x0c,0x01])
	writeByte([0x0f,0x00,0x0f,0x00])

def write(leftData, rightData, size = 8):
	for i in range(0, size):
		_data = []
		_data.append(i + 1)
		_data.append(rightData[i])
		_data.append(i + 1)
		_data.append(leftData[i])
		writeByte(_data)

def blink(times = 2):
	for _ in range(0,times):
		write(full, full)
		time.sleep(0.5)
		write(clear, clear)
		time.sleep(0.5)

def showNum(num):
	if not isinstance(num, int):
		return
	_num = num
	if(_num > 100):
		_num = _num % 100
	leftNum = 0
	if(_num >= 10):
		leftNum = _num // 10
	rightNum = _num % 10
	write(numList[leftNum], numList[rightNum])

# 配置初始化
def setup():
	#GPIO.setwarnings(False) # 禁用GPIO警告显示
	GPIO.setmode(GPIO.BCM) # 使用BCM编码
	GPIO.setup(Max7219_pinCS, GPIO.OUT) # 设定为输出通道

	#设置外围电路
	GPIO.setup(Button_VCCPin, GPIO.OUT)
	GPIO.output(Button_VCCPin, GPIO.HIGH)
	GPIO.setup(Button_inputPin, GPIO.IN)

	initMAX7219()

def loop():
	num = 0
	blink()
	while(True):
		if(GPIO.input(Button_inputPin) == GPIO.LOW):
			print("按钮按下")
			while (True):
				if(GPIO.input(Button_inputPin) == GPIO.HIGH):
					if(num >= 100):
						num -= 100
					print("按钮弹起，显示数字%d" % num)
					showNum(num)
					num += 1
					break
				time.sleep(0.1)
		time.sleep(0.1)



if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt, e:
		print("program interrupt")
		spi.close()
		GPIO.cleanup(); # 恢复状态
	finally:
		spi.close()
		GPIO.cleanup(); # 恢复状态