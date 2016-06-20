#coding:utf-8

import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr

        # token
        token="moonrailgun"

        # 字典排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update, list)
        hashcode=sha1.hexdigest()

        # 如果是微信的请求。回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text

        if content == u"排队":
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"正在排队中。请稍后")
        elif content == u"翻译":
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"请输入【翻译 文字】这样的格式")
        else:
            helpFile = open("help.txt")
            try:
                helpStr = helpFile.read()
                return self.render.reply_text(fromUser,toUser,int(time.time()),helpStr)
            finally:
                helpFile.close()