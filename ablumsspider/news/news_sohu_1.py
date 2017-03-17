#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import types
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class news_sohu_1():
    def __init__(self):
        print "Do spider news_sohu_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p101_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p101_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p102_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p103_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p104_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p105_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p106_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p107_p11_p12_p13.html",
                         "http://so.tv.sohu.com/list_p1122_p2_p3_p486400_p5_p6_p7_p8_p9_p108_p11_p12_p13.html",

        ]
        self.pidList = {}
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "news_sohu_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            detail = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            detail_p = soup.find("ul", attrs={"class": "st-list short cfix"})
            if detail_p is not None:
                detail = detail_p.find_all("li")
            for each in detail:
                self.seedSpider(each)

    def seedSpider(self, detail):
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(detail)
            self.program["ptype"] = "新闻".decode("utf8")
            self.program['website'] = '搜狐'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                return

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, detail):
        name = ""
        poster = ""
        point = 0.0
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        pcUrl = ""
        mainId = ""
        area = ""

        div_tag = detail.find("div", attrs={"class": "st-pic"})
        if div_tag is None:
            return
        a_tag = div_tag.find("a", attrs={"target": "_blank"})
        if a_tag is None:
            return


        img = a_tag.find("img")
        if img is not None:
            poster_P = img.get("src")
            if poster_P is not None:
                poster = "http:%s" % poster_P
            name_P = img.get("alt")
            if name_P is not None:
                name = name_P

        pcUrl_P = a_tag.get("href")
        if pcUrl_P is not None:
            pcUrl = "http:%s" % pcUrl_P

        doc = spiderTool.getHtmlBody(pcUrl)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        ctype_P = soup.find('div', attrs={'class': 'crumbs'})
        if ctype_P is not None:
            a_list = []
            for a_tag in ctype_P.find_all('a'):
                a_list.append(a_tag.get_text())
            a_str = ",".join(a_list)
            ctype = a_str

        mainId_P = re.search(r'http://tv\.sohu\.com/\d+/(\w+)\.shtml', pcUrl)
        if mainId_P:
            mainId = time.strftime('%Y%m%d',time.localtime(time.time())) + mainId_P.group(1)

        shootYear = time.strftime('%Y',time.localtime(time.time()))
        intro = name


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['point'] = point
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['pcUrl'] = pcUrl
        self.program['mainId'] = mainId

        self.secondSpider(pcUrl, name, poster)
    def secondSpider(self, pcUrl, name, poster):
            setName = name
            webUrl = pcUrl
            setNumber = time.strftime('%Y%m%d',time.localtime(time.time()))
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                return
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = news_sohu_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()