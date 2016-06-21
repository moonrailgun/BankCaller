#coding:utf-8

import RPi.GPIO as GPIO
import spidev
import time

Max7219_pinCS = 24
data = [[0x3c,0x42,0x42,0x42,0x42,0x42,0x42,0x3c]]
#data = [[0xff,0x00,0x00,0x00,0x00,0x00,0x00,0xff]]
#data = [[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]]
spi = spidev.SpiDev()
spi.open(0,0)#bus, device
spi.mode = 0

def writeByte(_data):
	GPIO.output(Max7219_pinCS, GPIO.LOW) # 输出低电平
	#spi.xfer(_data)
	spi.writebytes(_data)
	GPIO.output(Max7219_pinCS, GPIO.HIGH) # 输出高电平

	print(_data)
	# time.sleep(0.01) #delay 1s

# 初始化MAX7219模块
def initMAX7219():
	writeByte([0x09,0x00,0x09,0x00])
	writeByte([0x0a,0x03,0x0a,0x03])
	writeByte([0x0b,0x07,0x0b,0x07])
	writeByte([0x0c,0x01,0x0c,0x01])
	writeByte([0x0f,0x00,0x0f,0x00])

# 配置初始化
def setup():
	#GPIO.setwarnings(False) # 禁用GPIO警告显示
	GPIO.setmode(GPIO.BCM) # 使用BCM编码
	GPIO.setup(Max7219_pinCS, GPIO.OUT) # 设定为输出通道

	initMAX7219()

def loop():
	while(True):
		for i in range(0, len(data[0])):
			_data = []
			_data.append(i + 1)
			_data.append(data[0][i])
			_data.append(i + 1)
			_data.append(data[0][i])
			writeByte(_data)
		print("---")
		time.sleep(1)


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