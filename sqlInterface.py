#coding:utf-8

import sqlite3
import time

class SQLInterface:
	def getConnect(self):
		return sqlite3.connect('./db/data.db')

	def execute(self, sql):
		conn = self.getConnect()
		cursor = conn.execute(sql)
		ret = cursor.fetchall()
		conn.commit()
		conn.close()
		return ret

	def init(self):
		print u"开始初始化数据库"
		self.execute('''CREATE TABLE IF NOT EXISTS we_chat
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id TEXT NOT NULL,
			serial_number INTEGER NOT NULL,
			is_finish INTEGER NOT NULL,
			created_at TEXT NOT NULL);''')
		print u"数据库初始化完毕"

class CallerSQL:
	def addToQueue(self, user_id):
		nowTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		maxSerial = self.getMaxSerialNumber()
		allocSerial = maxSerial + 1
		ret = SQLInterface().execute('INSERT INTO we_chat(user_id,serial_number,is_finish,created_at) VALUES("%s","%s",%d,"%s")' % (user_id, allocSerial,0,nowTime) )
		return allocSerial

	def getMaxSerialNumber(self):
		ret = SQLInterface().execute('SELECT MAX(serial_number) FROM we_chat')
		serial = ret[0][0]
		if(serial == None):
			serial = 0
		return serial

	def getUnfinishSerial(self):
		ret = SQLInterface().execute('SELECT MIN(serial_number) FROM we_chat WHERE is_finish = 0')
		serial = ret[0][0]
		if(serial == None):
			serial = -1
		return serial

	#完成最近的一条序列
	def finishOneSerial(self):
		serial = self.getUnfinishSerial()
		SQLInterface().execute('UPDATE we_chat SET is_finish = 1 WHERE serial_number = %d' % serial)
	
	#获取未完成的序列个数
	def getUnfinishSerialCount(self):
		ret = SQLInterface().execute('SELECT COUNT(*) FROM we_chat WHERE is_finish = 0')
		serial = ret[0][0]
		if(serial == None):
			serial = 0
		return serial


if __name__ == '__main__':
	SQLInterface().init()