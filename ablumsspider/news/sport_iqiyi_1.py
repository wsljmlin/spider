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


class sport_iqiyi_1():
    def __init__(self):
        print "Do spider sport_iqiyi_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.iqiyi.com/www/17/-------------4-1-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-1-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-2-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-3-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-4-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-5-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-6-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-7-2-iqiyi--.html",
                         "http://list.iqiyi.com/www/17/-------------4-8-2-iqiyi--.html",

        ]
        self.pidList = {}
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "sport_iqiyi_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            detail = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            detail_p = soup.find("ul", attrs={"class": "site-piclist site-piclist-180101 site-piclist-auto"})
            if detail_p is not None:
                detail = detail_p.find_all("li")
            for each in detail:
                self.seedSpider(each)

    def seedSpider(self, detail):
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(detail)
            self.program["ptype"] = "体育".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
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

        public = ""
        div_public = detail.find("div", attrs={"class": "site-piclist_info"})
        if div_public is not None:
            public_P = div_public.find('div', attrs={"class": "role_info"})
            if public_P is not None:
                public = public_P.get_text().strip()

        if re.search(r'\d+-\d+-\d+', public):
            shootYear = public.split("-")[0]
        else:
            public = ""

        div_tag = detail.find("div", attrs={"class": "site-piclist_pic"})
        if div_tag is None:
            return
        a_tag = div_tag.find("a", attrs={"target": "_blank"})
        if a_tag is None:
            return


        img = a_tag.find("img")
        if img is not None:
            poster_P = img.get("src")
            if poster_P is not None:
                poster = poster_P
            name_P = img.get("alt")
            if name_P is not None:
                name = name_P

        pcUrl_P = a_tag.get("href")
        if pcUrl_P is not None:
            pcUrl = pcUrl_P

        mainId_P = re.search(r'http://www\.iqiyi\.com/(\w+)\.html', pcUrl)
        if mainId_P:
            mainId = mainId_P.group(1)

        if shootYear != "":
            mainId = public.replace('-', '') + mainId

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

        self.secondSpider(pcUrl, name, poster, public)
    def secondSpider(self, pcUrl, name, poster, public):
            setName = name
            webUrl = pcUrl
            if public != "":
                setNumber = public.replace('-', '')
            else:
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
    app = sport_iqiyi_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()