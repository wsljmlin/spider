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


class amuse_youku_1():
    def __init__(self):
        print "Do spider amuse_youku_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.youku.com/category/video/c_86_d_1_s_2_p_1.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_1.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_2.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_3.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_4.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_5.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_6.html",
                         "http://list.youku.com/category/video/c_86_d_1_s_2_p_7.html",
        ]
        self.pidList = {}
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "amuse_youku_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            detail = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            detail_p = soup.find("div", attrs={"class": "yk-row"})
            if detail_p is not None:
                detail = detail_p.find_all("div", attrs={"class": "yk-col4"})
            for each in detail:
                self.seedSpider(each)

    def seedSpider(self, detail):
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(detail)
            self.program["ptype"] = "娱乐".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets'], self.program['mainId']
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

        div_tag = detail.find("div", attrs={"class": "p-thumb"})
        if div_tag is None:
            return
        a_tag = div_tag.find("a", attrs={"target": "_blank"})
        if a_tag is None:
            return


        img = div_tag.find("img")
        if img is not None:
            poster_P = img.get("src")
            if poster_P is not None:
                poster = poster_P
            name_P = img.get("alt")
            if name_P is not None:
                name = name_P

        pcUrl_P = a_tag.get("href")
        if pcUrl_P is not None:
            pcUrl = "http:%s" % pcUrl_P

        mainId_P = re.search(r'http://v.youku.com/v_show/id_(.+)==', pcUrl)
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
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
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
    app = amuse_youku_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()