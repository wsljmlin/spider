#!/usr/bin/env python
#encoding=UTF-8
import urllib2
import time
import re
import os
import chardet
CN_NUM = {
u'〇' : 0,
u'一' : 1,
u'二' : 2,
u'三' : 3,
u'四' : 4,
u'五' : 5,
u'六' : 6,
u'七' : 7,
u'八' : 8,
u'九' : 9,

u'零' : 0,
u'壹' : 1,
u'贰' : 2,
u'叁' : 3,
u'肆' : 4,
u'伍' : 5,
u'陆' : 6,
u'柒' : 7,
u'捌' : 8,
u'玖' : 9,

u'貮' : 2,
u'两' : 2,
}
CN_UNIT = {
u'十' : 10,
u'拾' : 10,
u'百' : 100,
u'佰' : 100,
u'千' : 1000,
u'仟' : 1000,
u'万' : 10000,
u'萬' : 10000,
u'亿' : 100000000,
u'億' : 100000000,
u'兆' : 1000000000000,
}



class spiderTool():
    def __init__(self):
        pass

    @staticmethod
    def getHtmlBody(url):
        retryTimes = 1
        timeInterval = 3
        headers_set = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie': 'ppi=302c31'}
        if url == "":
            print "Error: Url."
            exit()
        requestUrl = url
        doc = ""
        while doc == "" and retryTimes > 0:
            try:
                req = urllib2.Request(requestUrl, headers=headers_set)
                socket = urllib2.urlopen(req, timeout=10)
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

    @staticmethod
    def cn2dig(cn):
        lcn = list(cn)
        unit = 0 #当前的单位
        ldig = []#临时数组

        while lcn:
            cndig = lcn.pop()
            if CN_UNIT.has_key(cndig):
                unit = CN_UNIT.get(cndig)
                if unit==10000:
                    ldig.append('w')    #标示万位
                    unit = 1
                elif unit==100000000:
                    ldig.append('y')    #标示亿位
                    unit = 1
                elif unit==1000000000000:#标示兆位
                    ldig.append('z')
                    unit = 1
                continue
            else:
                dig = CN_NUM.get(cndig)
                if unit:
                    dig = dig*unit
                    unit = 0
                ldig.append(dig)
        if unit==10:    #处理10-19的数字
            ldig.append(10)
        ret = 0
        tmp = 0
        while ldig:
            x = ldig.pop()
            if x=='w':
                tmp *= 10000
                ret += tmp
                tmp=0
            elif x=='y':
                tmp *= 100000000
                ret += tmp
                tmp=0
            elif x=='z':
                tmp *= 1000000000000
                ret += tmp
                tmp=0
            else:
                tmp += x
        ret += tmp
        return str(ret)


