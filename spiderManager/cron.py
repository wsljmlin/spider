#!/usr/bin/env python
#encoding=UTF-8
import sys
import os
import time
import re
import types
import json
from model.spiderCron import spiderCron
from model.mysqldb import db
from config import spiderModelPath
from config import runtimeSave
from spiderModel.spiderTool import spiderTool
sys.path.append(spiderModelPath)


class cron():
    def __init__(self):
        self.runTime = ""
        self.fileName = 'data' + os.path.sep + time.strftime('cron_manager_spider_%Y%m%d%H%M%S.txt', time.localtime(time.time()))
        self.openFile = open(self.fileName,'w')

    def __del__(self):
        self.openFile.close()

    def run(self):
        getUrl = "http://localhost:9527/spider/cronData?runTime=" + self.runTime
        data = spiderTool.getHtmlBody(getUrl)
        if data == "":
            return ""
        dataList = json.loads(data)
        modelList = os.listdir(spiderModelPath)
        for each in dataList:
            spider = each['spider']
            url = each['url']
            if spider == "" or url == "":
                continue
            if spider + ".py" not in modelList:
                continue
            else:
                try:
                    spider_module = __import__(spider)
                    spider_class = eval("spider_module." + spider + "()")
                except:# IOError, e:
                    spider_class = ""

            if spider_class != "":
                try:
                    spider_class.seedList = [url]
                    spider_class.seedSpider()
                    jsonData = spider_class.jsonData
                except:# IOError, e:
                    jsonData = ""
            else:
                jsonData = ""
            if jsonData != "":
                self.openFile.write(str(jsonData))

if __name__ == "__main__":
    app = cron()
    if len(sys.argv) > 1:
        app.runTime = sys.argv[1]
        app.run()