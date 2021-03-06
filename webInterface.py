#coding:utf-8

import web
import os

from weixinInterface import WeixinInterface

urls = ('/weixin', 'WeixinInterface')

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals())

if __name__ == '__main__':
	app.run()

# app = web.application(urls, globals()).wsgifunc()
# application = sae.create_wsgi_app(app)