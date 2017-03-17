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
class weixindianying():
    def __init__(self):
        print "Do spider weixindianying."
        self.data = {}
        self.seedBase = ["http://www.ppypp.com/dy/index.html"]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "weixindianying" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for i in range(2239, 2863):
            print "page :" + str(i)
            self.seedBase = []
            self.seedBase.append('http://www.ppypp.com/dy/index'+str(i)+'.html')
            for seed in self.seedBase:
                self.seedList = []
                seedList = []
                doc = spiderTool.getHtmlBody(seed)
                soup = BeautifulSoup(doc, from_encoding="utf8")
                seed_P = soup.find("div", attrs={"class": "index-area clearfix"})
                if seed_P is not None:
                    seedList = seed_P.find_all("li", attrs={"class": "p1 m1"})
                for each in seedList:
                    a_tag = each.find("a")
                    if a_tag is not None:
                        subSeed = a_tag.get("href")
                        if subSeed is not None:
                            self.seedList.append("http://www.ppypp.com"+subSeed)
                self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.data = {}
            self.firstSpider(seed)
            if self.data.has_key('title') is False:
                continue
            if self.data['title'] == '' or self.data['title'] is None \
                or (self.data['ykyun'] == ''and self.data['geda'] == ""):
                continue
            print self.data['title'], self.data['ykyun'], self.data['geda']
            strData = json.dumps(self.data)

            self.dataFile.write(strData + '\n')
            self.getHtmlBody()


    def firstSpider(self, seed):
        point = 0.0
        poster = ""
        pcUrl = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        playLength = ""
        programLanguage = ""
        mainId = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        if seed != '':
            pcUrl = seed

        point_P = soup.find('dt',attrs={'class': 'score_num_wrap clearfix'})
        if point_P is not None:
            point = point_P.find('strong').get_text()

        poster_p = soup.find("div",attrs={'class':'ct-l'})
        if poster_p is not None:
            poster_img = poster_p.find('img')
            if poster_img is not None:
                poster = poster_img.get("data-original")
                name = poster_img.get("alt")
        if name is None:
            name = ""
        if poster is None:
            poster = ""

        intro_p = soup.find("div", attrs={"class": "ct-c"})
        if intro_p is not None:
            intro_text = intro_p.find("div", attrs = {"class": "ee", "name":"ee"})
            if intro_text is not None:
                intro = intro_text.get_text().replace("PPYPP影院：".decode('utf8'), "")
        else:
            return

        detail = intro_p.find("dl")
        if detail is not None:
            items = detail.find_all("dd")
            for item in items:
                a_list = []
                for each in item.find_all('a'):
                    a_list.append(each.get_text())
                a = ",".join(a_list)
                item_text = item.get_text()
                if re.search('别名：'.decode('utf8'), item_text):
                    alias = item_text.replace('别名：'.decode('utf8'), '').replace(' / '.decode('utf8'), ',')
                if re.search('时长：(\d+)'.decode('utf8'), item_text):
                    playLength = re.search('时长：(\d+)'.decode('utf8'), item_text).group(1) + ":00"
                if re.search('地区：'.decode('utf8'), item_text):
                    area = re.search(r'地区：(.*?)\n'.decode('utf8'), item_text).group(1)
                if re.search('年份：(\d+)'.decode('utf8'), item_text):
                    shootYear = re.search('年份：(\d+)'.decode('utf8'), item_text).group(1)
                if re.search(r'语言：'.decode('utf8'), item_text):
                    programLanguage = item_text.split('语言：'.decode('utf8'))[1]
                if re.search(r'豆瓣评分：(\d+\.\d+)'.decode('utf8'), item_text):
                    point = re.search('豆瓣评分：(\d+\.\d+)'.decode('utf8'), item_text).group(1)
                if re.search('主演：'.decode('utf8'), item_text):
                    star = a
                if re.search('导演：'.decode('utf8'), item_text):
                    director = a

        self.data = {"channelid":"17", "dopost":"save","qingxi":"高清".decode('utf8'),"weight":"200","typeid":"1","ishtml":"1","autolitpic":'1',"remote":'1',"writer":"admin",
                "dede_addonfields":"nianfen,text;zhuyan,text;daoyan,text;diqu,text;leibie,text;yuyan,text;juqing,multitext;qingxi,text;vurl,text;lsvid,text;geda,multitext;lspan,multitext;ykyun,text"
        }
        self.data["juqing"] = intro
        self.data["nianfen"] =shootYear
        self.data["title"] = spiderTool.changeName(name)
        self.data["yuyan"] = programLanguage
        self.data["daoyan"] = director.replace(",", "、".decode('utf8'))
        self.data["diqu"] = area
        self.data["picname"] = poster
        self.data["zhuyan"] = star.replace(",", "、".decode('utf8'))
        self.data['ykyun'] = ""
        self.data['geda'] = ""
        for vk in range(1, 4):
            vclass = "vlink_" + str(vk)
            vlink = soup.find('div', attrs={'id': vclass})
            if vlink is not None and self.data['ykyun'] == "" and self.data['geda'] == "":
                a_href = vlink.find_all('a', attrs={'target':'_self'})
                for a in a_href:
                    subSeed = a.get('href')
                    if subSeed is not None:
                        self.secondSpider(subSeed)
    def secondSpider(self,seed):
        url = "http://www.ppypp.com" + seed
        doc = spiderTool.getHtmlBody(url)
        if re.search(r'unescape\("(.*?)"', doc):
            ykyun_url =  re.search(r'unescape\("(.*?)"', doc).group(1)
            ykyun_doc = urllib.unquote_plus(ykyun_url).replace('%u','\\u').decode("unicode_escape").decode('utf8')
            if re.search(r'优酷云\$\$\w{0,2}高清\$(.*?)\$ykyun'.decode('utf8'), ykyun_doc):
                ykyun = re.search(r'优酷云\$\$\w{0,2}高清\$(.*?)\$ykyun'.decode('utf8'), ykyun_doc).group(1)
                self.data['ykyun'] = ykyun
            elif re.search(r'http://www\.bilibili\.com(.*?)\$bilibili'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://www\.bilibili\.com(.*?)\$bilibili'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://www.bilibili.com" + bd
            elif re.search(r'http://www\.1905\.com(.*?)\$m1905'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://www\.1905\.com(.*?)\$m1905'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://www.1905.com" + bd
            elif re.search(r'http://www\.fun\.tv(.*?)\$fun'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://www\.fun\.tv(.*?)\$fun'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://www.fun.tv" + bd
            elif re.search(r'http://v\.pptv\.com(.*?)\$pptv'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://v\.pptv\.com(.*?)\$pptv'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://v.pptv.com" + bd
            elif re.search(r'http://www\.iqiyi\.com(.*?)\$qiyi'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://www\.iqiyi\.com(.*?)\$qiyi'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://www.iqiyi.com" + bd
            elif re.search(r'http://www\.acfun\.tv(.*?)\$acfun'.decode('utf8'), ykyun_doc):
                bd = re.search(r'http://www\.acfun\.tv(.*?)\$acfun'.decode('utf8'), ykyun_doc).group(1)
                self.data['geda'] = "http://www.acfun.tv" + bd

    def getHtmlBody(self):
        cTime = str(int(time.time()))
        cookie = "menuitems=1_1%2C2_1%2C3_1; PHPSESSID=2hg84d73990r4hfoi4pv8mn3b0; DedeUserID=1; DedeUserID__ckMd5=1d8b0140276a1511; DedeLoginTime=" + cTime + "; DedeLoginTime__ckMd5=715a2ae437968dba; ENV_GOBACK_URL=%2Fdianshi%2Fcontent_list.php%3Fchannelid%3D17"
        headers_set = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Cookie': cookie}
        requestUrl = "http://www.dianshifen.net/dianshi/archives_add.php"
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

if __name__ == '__main__':
    app = weixindianying()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()



