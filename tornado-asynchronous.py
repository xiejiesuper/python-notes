 # -*- coding: UTF-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import urllib
import json
import os
import time
import pymongo
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

def inlineMakeErrorDic(err,code,next_retry_time=60):
    return json.dumps({'error':err,'error_code':code,'next_retry_time' : next_retry_time})

def getuser(token):
    return token.split(':')[0]
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]

        conn = pymongo.MongoClient("127.0.0.1", 27017)
        self.db = conn["camera_base"]
        tornado.web.Application.__init__(self, handlers)   

class IndexHandler(tornado.web.RequestHandler):
    executor = ProcessPoolExecutor(5)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        token  = self.get_argument('token')
        tvid = self.get_argument('tvid')
        if not(token or tvid) or (token and tvid):
            self.write(inlineMakeErrorDic('wrong parameter',400))
        else:
       
            if token:
                ret = self.application.db.binddev.find({'user':getuser(token)},{'name':1,'user':1,'ukey':1})
            else:
                ret = self.application.db.binddev.find({'tvid':tvid},{'name':1,'user':1,'ukey':1})
            tmp =[]
            for i in ret:
                if i['ukey'] == '':
                    r1 = self.application.db.ukey.find_one({"_id":i['_id']})
                    if r1:
                        i['ukey'] = r1['ukey']
                        self.application.db.binddev.save(i)
                devstatus = {}
                devstatus['devid'] = i['_id']
                devstatus['ukey'] = i['ukey']
                retStat = self.application.db.devstatus.find_one({"_id":i['_id']})
                if retStat == None or (int(time.time()) - retStat['time']) >300:
                    res = yield self.chkstatus(i['ukey'])
                    if res == 1:
                        devstatus['online'] = 'yes'
                    else:
                        devstatus['online'] = 'no'
                    devnow = {}
                    devnow['_id'] = i['_id']
                    devnow['ukey'] = i['ukey']
                    devnow['online'] = devstatus['online']
                    if retStat:
                        devnow['count'] = retStat['count']+1
                    else:
                        devnow['count'] = 1
                    devnow['time'] = int(time.time())
                    self.application.db.devstatus.save(devnow)
                else:
                    devstatus['online'] = retStat['online']
                tmp.append(devstatus)
            if token:
              ret2 = self.application.db.bindaccredit.find({'guest':getuser(token)},{'devid':1,'host':1,'ukey':1,"_id":0})
              for i in ret2:
                if i['ukey'] == '':
                    r1 = self.application.db.ukey.find_one({"_id":i['devid']})
                    if r1:
                        i['ukey'] = r1['ukey']
                        self.application.db.binddev.save(i)
                devstatus = {}
                devstatus['devid'] = i['devid']
                devstatus['ukey'] = i['ukey']

                retStat = self.application.db.devstatus.find_one({"_id":i['devid']})
                if retStat == None or (int(time.time()) - retStat['time']) >300:
                    res1 = yield self.chkstatus(i['ukey'])
                    if res1 == 1:
                        devstatus['online'] = 'yes'
                    else:
                        devstatus['online'] = 'no'
                    devnow = {}
                    devnow['_id'] = i['devid']
                    devnow['online'] = devstatus['online']
                    devnow['time'] = int(time.time())
                    devnow['ukey'] = i['ukey']
                    if retStat:
                        devnow['count'] = retStat['count']+1
                    else:
                        devnow['count'] = 1
                    self.application.db.devstatus.save(devnow)
                else:
                    devstatus['online'] = retStat['online']

                tmp.append(devstatus)

            tmp2 = {}
            tmp2['code'] = 0
            tmp2['token'] = token
            tmp2['data']  = tmp
            tmp2['tvid'] = tvid
            self.write(json.dumps(tmp2))
            self.finish()

    @run_on_executor
    def chkstatus(self,ukey):
        cmdline = '/opt/api_uwsgi/galacam/galacam/ppp_test %s'% ukey
        ret = os.system(cmdline)
        ret = ret>>8
        return ret

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()