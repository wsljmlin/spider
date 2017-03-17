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

class all_ppypp_tv():
    def __init__(self):
        print "Do spider all_ppypp_tv."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://www.ppypp.com/ds/index.html"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_ppypp_tv_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for i in range(2, 595):
            self.seedBase.append('http://www.ppypp.com/ds/index'+str(i)+'.html')
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
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = 'ppypp'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

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


        if re.match(r'http://www.ppypp.com/ds/(\w+)/', seed):
            mainId = "ppypp_dy_" + re.match(r'http://www.ppypp.com/ds/(\w+)/', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['pcUrl'] = pcUrl
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['programLanguage'] = programLanguage
        self.program['mainId'] = mainId
        self.program_sub['playLength'] = playLength + ':' + '00'
        self.secondSpider(doc)

    def secondSpider(self,doc):
        soup = BeautifulSoup(doc, from_encoding="utf8")
        data = soup.find('div', attrs={"class": "videourl clearfix"})
        if data is None:
            return
        for item in data.find_all("a"):
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            if item.get("title") is not None:
                setName = item.get("title")
                if re.search(r'(\d+)', setName):
                    setNumber = re.search(r'(\d)', setName).group(1)
            if item.get('href') is not None:
                webUrl = "http://www.ppypp.com" + item.get('href')
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program['programSub'].append(self.program_sub)
if __name__ == '__main__':
    app = all_ppypp_tv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()