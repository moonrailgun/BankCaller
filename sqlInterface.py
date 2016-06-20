#coding:utf-8

import sqlite3

class SQLInterface:
	def getConnect(self):
		return sqlite3.connect('./db/data.db')

	def execute(self, sql):
		conn = self.getConnect()
		conn.execute(sql)
		conn.close()

	def init(self):
		print u"开始初始化数据库"
		self.execute('''CREATE TABLE IF NOT EXISTS we_chat
			(id INT PRIMARY KEY NOT NULL,
			user_id TEXT NOT NULL,
			serial_number TEXT NOT NULL,
			is_finish INT NOT NULL,
			created_at TEXT NOT NULL);''')
		print u"数据库初始化完毕"

if __name__ == '__main__':
	SQLInterface().init()