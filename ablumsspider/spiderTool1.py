#!/usr/bin/env python
#encoding=UTF-8
import urllib2
import time
import re
import os
import chardet

class spiderTool():
    def __init__(self):
        pass

    @staticmethod
    def getHtmlBody(url):
        retryTimes = 5
        timeInterval = 8
        headers_set = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        if url == "":
            print "Error: Url."
            exit()
        requestUrl = url
        doc = ""
        while doc == "" and retryTimes > 0:
            try:
                proxy = "http://123.118.17.140:808"
                proxy_handler = urllib2.ProxyHandler({'http': proxy})
                req = urllib2.Request(requestUrl, headers=headers_set)
                opener = urllib2.build_opener(proxy_handler)
                socket = opener.open(req, timeout=10)
                headers = socket.info()
                doc = socket.read()
                if ('Content-Encoding' in headers and headers['Content-Encoding']) or \
                        ('content-encoding' in headers and headers['content-encoding']):
                    import gzip
                    import StringIO
                    data = StringIO.StringIO(doc)
                    gz = gzip.GzipFile(fileobj=data)
                    doc = gz.read()
                    gz.close()
                socket.close()
                retryTimes -= 1
            except:
                print "urllib2.HTTPError:Internal Server Error"
                retryTimes -= 1
                time.sleep(timeInterval)
        return doc

    @staticmethod
    def getProxyHtmlBody(proxy, url):
        retryTimes = 2
        timeInterval = 5
        if proxy == "":
            print "Error: Proxy."
            exit()
        if url == "":
            print "Error: Url."
            exit()
        requestUrl = proxy + "/" + url
        doc = ""
        while doc == "" and retryTimes > 0:
            print "aaaaa"
            try:
                request = urllib2.urlopen(requestUrl)
                doc = request.read()
                retryTimes -= 1
            except:
                print "urllib2.HTTPError:Internal Server Error"
                retryTimes -= 1
                time.sleep(timeInterval)
        return doc

    @staticmethod
    def listStringToJson(name, listString):
        rt = []
        if listString == "":
            return []
        listString = listString.replace("，".decode("utf8"), ",")
        if name != 'url':
            listString = listString.replace("/".decode("utf8"), ",")
        for each in listString.split(","):
            rt.append({name:each})
        return rt

    @staticmethod
    def changeName(name):
        #去掉两边空格,中间空格不管
        final_name = name.strip()
        #中文冒号:英文冒号
        final_name = final_name.replace("：".decode("utf8"), ":")
        #中文小括号:英文小括号
        final_name = final_name.replace("（".decode("utf8"), "(")
        final_name = final_name.replace("）".decode("utf8"), ")")
        #中括号:小括号
        final_name = final_name.replace("[".decode("utf8"), "(")
        final_name = final_name.replace("]".decode("utf8"), ")")
        #中文逗号：英文逗号
        final_name = final_name.replace("，".decode("utf8"), ",")
        #横杠:空
        final_name = final_name.replace("-".decode("utf8"), "")
        #文双引号:英文双引号
        final_name = final_name.replace("“".decode("utf8"), "\"")
        final_name = final_name.replace("”".decode("utf8"), "\"")
        #中文问号:英文问号
        final_name = final_name.replace("？".decode("utf8"), "?")
        #中文顿号:英文逗号!
        final_name = final_name.replace("、".decode("utf8"), ",")
        #中文感叹号:英文感叹号
        final_name = final_name.replace("！".decode("utf8"), "!")
        #中文中括号:英文小括号
        final_name = final_name.replace("【".decode("utf8"), "(")
        final_name = final_name.replace("】".decode("utf8"), ")")
        #多个空格或制表符替换为一个空格
        final_name = re.sub(r'\s+'.decode("utf8"), ' ', final_name)
        #多个单引号替换为一个单引号
        final_name = re.sub(r'\'+'.decode("utf8"), '\'', final_name)
        #去掉末尾反斜杠
        final_name = re.sub(r'\\+$'.decode("utf8"), '', final_name)
        return final_name

    @staticmethod
    def openFile(dataFile):
        try:
            openFile = open(dataFile, 'w')
            return openFile
        except:
            print "file open error!"
        return None

    @staticmethod
    def closeFile(dataFile):
        if dataFile is not None:
            dataFile.close()

    @staticmethod
    def readSeedList(seedFile):
        seedList = []
        if os.path.isfile(seedFile) is False:
            return seedList
        openFile = open(seedFile, 'r')
        seedLines = openFile.readlines()
        for line in seedLines:
            seedList.append(line)
        return seedList



