#coding:utf-8

import RPI.GPIO as GPIO
import spidev
import time

led_pin = 24

def setup:
	GPIO.setwarnings(False) # 禁用GPIO警告显示
	GPIO.setmode(GPIO.BCM) # 使用BCM编码
	GPIO.setup(led_pin, GPIO.OUT) # 设定为输出通道

def loop:
	pass

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt, e:
		GPIO.cleanup(); # 恢复状态
