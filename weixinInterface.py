#coding:utf-8

import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import get_cpu_temp
from sqlInterface import SQLInterface
from sqlInterface import CallerSQL

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
            remain = CallerSQL().getUnfinishSerialCount()
            serial = CallerSQL().addToQueue(fromUser)
            msg = u"正在排队中，您分配到的编号为%d。"%serial
            if(remain > 0):
                msg += u"请稍后，您前方尚有%d人" % remain
            else:
                msg += u"工作窗口正空，请马上去窗口报道"
            return self.render.reply_text(fromUser,toUser,int(time.time()),msg)
        elif content == u"温度":
            cpu_temp = get_cpu_temp.get_cpu_temp()
            gpu_temp = get_cpu_temp.get_gpu_temp()
            str = "服务器温度:\nCPU:%.1f\nGPU:%.1f" % (cpu_temp, gpu_temp)
            return self.render.reply_text(fromUser,toUser,int(time.time()),str)
        elif content == u"翻译":
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"请输入【翻译 文字】这样的格式")
        else:
            helpFile = open("help.txt")
            try:
                helpStr = helpFile.read()
                return self.render.reply_text(fromUser,toUser,int(time.time()),helpStr)
            finally:
                helpFile.close()