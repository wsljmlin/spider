#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import urllib
import urllib2
import types
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
class weixindianying404():
    def __init__(self):
        print "Do spider weixindianying404."
        self.data = {}
        self.seedBase = ["http://www.ppypp.com/dy/index.html"]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "weixindianying404_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for i in range(1, 220):
            url = "http://www.dianshifen.net/dianshi/content_list.php?dopost=listArchives&keyword=&cid=0&flag=&orderby=id&arcrank=&channelid=17&f=form1.arcid1&totalresult=6156&pageno="
            print "page :" + str(i)
            self.seedBase = []
            self.seedBase.append(url + str(i))
            for seed in self.seedBase:
                self.seedList = []
                seedList = []
                doc = self.getHtmlBody(seed)
                soup = BeautifulSoup(doc, from_encoding="utf8")
                seedList = soup.find_all("tr", attrs={"align": "center", "height":"26"})
                for each in seedList:
                    a_tag = each.find("input", attrs={"name": "arcID"})
                    if a_tag is not None:
                        subSeed = a_tag.get("value")
                        if subSeed is not None:
                            self.seedList.append("http://www.dianshifen.net/dianshi/archives_edit.php?aid="+subSeed)
                self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.data = {}
            self.firstSpider(seed)
            print self.data['id'], self.data['name'], self.data['url'], self.data['404']
            if self.data['id'] == '' or self.data['id'] is None \
                or self.data['404'] is False:
                continue
            print self.data['id'], self.data['name'], self.data['url'], self.data['404']
            strData = self.data['id'] + "," + self.data['name'] + "," + self.data['url'] + "," + str(self.data['404'])
            self.dataFile.write(strData + '\n')

    def firstSpider(self, seed):
        id = ""
        url = ""
        name = ""

        id_r = re.search(r'(\d+)', seed)
        if id_r:
            id = id_r.group(1)

        doc = self.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        name_p = soup.find("table", attrs={'id': 'needset'})
        if name_p is not None:
            name_value = name_p.find("input", attrs={'id': 'title'})
            if name_value is not None:
                name = name_value.get('value')

        url_p = soup.find("textarea", attrs={'id': 'geda'})
        if url_p is not None:
            url = url_p.get_text()



        self.data["id"] = id
        self.data["name"] = name
        self.data["url"] = url
        self.data["404"] = self.secondSpider(url)


    def secondSpider(self,seed):
        if seed == "":
            return False

        code = self.getUrlCode(seed)
        if code == 404:
            return True
        return False


    def getHtmlBody(self, requestUrl):
        cTime = str(int(time.time()))
        #每次都需要修改PHPSESSID
        PHPSESSID="a6k3lcbenetvmj0si11qkrlg20"
        cookie = "menuitems=1_1%2C2_1%2C3_1; PHPSESSID=" + PHPSESSID +"; DedeUserID=1; DedeUserID__ckMd5=1d8b0140276a1511; DedeLoginTime=" + cTime + "; DedeLoginTime__ckMd5=715a2ae437968dba; ENV_GOBACK_URL=%2Fdianshi%2Fcontent_list.php%3Fchannelid%3D17"
        headers_set = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Cookie': cookie}
        post_data = urllib.urlencode(self.data)
        req = urllib2.Request(requestUrl, headers=headers_set)
        socket = urllib2.urlopen(req, data=post_data, timeout=10)
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
        return doc

    def getUrlCode(self, url):
        retryTimes = 2
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
        code = ""
        while doc == "" and retryTimes > 0:
            try:
                req = urllib2.Request(requestUrl, headers=headers_set)
                socket = urllib2.urlopen(req, timeout=10)
                code = socket.getcode()
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
            except urllib2.HTTPError,e:
                print "urllib2.HTTPError:Internal Server Error"
                retryTimes -= 1
                time.sleep(timeInterval)
                code = e.code
        return code

if __name__ == '__main__':
    app = weixindianying404()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()



