#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
import urllib
import urllib2

class ablum_yinyuetai_mv():
    def __init__(self):
        self.base=["http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=1&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=1&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=2&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=3&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=4&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=5&tab=allmv&parenttab=mv"
                   ,"http://mv.yinyuetai.com/all?pageType=page&sort=weekViews&page=6&tab=allmv&parenttab=mv"
                   ]
        self.seedList = []
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_yinyuetai_mv_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()


    def doProcess(self):
        for seed in self.base:
            self.seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            div_p = soup.find_all("div", attrs={"class": "thumb thumb_mv J_add_convenient_container"})
            for div in div_p:
                subseed = div.find('a').get('href')
                if subseed is not None and  subseed != "":
                    self.seedList.append(subseed)

            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program["ptype"] = "音乐".decode("utf8")
            self.program['pcUrl'] = seed
            self.program['website'] = '音悦台'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.firstSpider(seed)
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program["name"], self.program['totalSets']

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == '' or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                return

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')



    def firstSpider(self, seed):
        poster = ""
        star = ""
        director = ""
        ctype = ""
        shootYear = ""
        intro = ""
        mainId = ""
        area = ""
        name = ""
        programLanguage = ""
        point = -1.0
        doubanPoint = -1.0
        poster = ""
        playTimes = 0
        pcUrl = ""
        duration = ""
        alias = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        head = soup.find('head')

        meta_list = head.find_all('meta')
        for meta in meta_list:
            #get name
            if meta.get('property') == "og:title":
                name = meta.get('content')

            #get poster
            if meta.get('property') == "og:image":
                poster = meta.get('content')

            #get intro
            if meta.get('property') == "og:description":
                intro = meta.get('content')

            #get area
            if meta.get('property') == "og:area":
                area = meta.get('content')

        #get mainId
        if re.match(r'http://v\.yinyuetai\.com/video/(.*)', seed):
            mainId = re.match(r'http://v\.yinyuetai\.com/video/(.*)', seed).group(1)

        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url', poster)
        self.program['star'] = spiderTool.listStringToJson('name', star)
        self.program['director'] = spiderTool.listStringToJson('name', director)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        self.program["name"] = spiderTool.changeName(name)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)

        self.secondSpider()


    def secondSpider(self):
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        setNumber = ""
        setName = ""
        webUrl = ""
        poster = ""

        setNumber = 1
        setName = self.program['name']
        webUrl = self.program['pcUrl']

        if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == "" \
                or setNumber is None or setName is None or webUrl is None:
            return

        self.program_sub['setNumber'] = setNumber
        self.program_sub['setName'] = setName
        self.program_sub['webUrl'] = webUrl
        self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = ablum_yinyuetai_mv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()


