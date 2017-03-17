#!/usr/bin/env python
#encoding=UTF-8
import re
import json
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
#美女视频


class beauty_mmwu_1():
    def __init__(self):
        print "Do spider beauty_mmwu_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = [ 'http://www.mmwu.tv/vod/opt/new'
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "beauty_mmwu_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            list_p = soup.find('div', attrs={'class': 'box movie_list'})
            if list_p is not None:
                self.seedList = list_p.find_all('li')
                self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '互联网'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'], self.program['totalSets'], self.program['mainId']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        name = ""
        poster = ""
        pcUrl  = ""
        star = ""
        ctype = "美女".decode("utf8")
        shootYear = ""
        intro = ""
        mainId = ""
        area = ""
        point = 0.0
        playTimes = 0

        playLength = ""
        setNum = ""

        soup = seed
        atag = soup.find("a")
        if atag is None:
            return

        pcUrl = atag.get('href')

        poster_p = atag.find('img')
        if poster_p is not None:
            poster = poster_p.get('src')

        name_p = atag.find('p')
        if name_p is not None:
            name = "美女写真_".decode("utf8") + name_p.get_text()


        mainId_p = re.search(r'http://www\.mmwu\.tv/vod/(.*?)\.html', pcUrl)
        if mainId_p:
            mainId = mainId_p.group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['pcUrl'] = pcUrl
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        self.program['point'] = point
        self.program['playTimes'] = playTimes
        self.secondSpider( name, pcUrl, playLength, poster)

    def secondSpider(self,setName, webUrl, playLength, poster):
        setNumber = ""
        doc = spiderTool.getHtmlBody(webUrl)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        setNumber_p = soup.find('div', attrs={'class': 'right'})
        if setNumber_p is not None:
            text = setNumber_p.get_text()
            setNumber_re = re.search(r'\d{4}-\d{2}-\d{2}', text)
            if setNumber_re:
                setNumber = setNumber_re.group().replace('-', '')
        if setNumber == "":
            setNumber = time.strftime('%Y%m%d',time.localtime(time.time()))
        if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                or setNumber is None or setName is None or webUrl is None:
            return
        self.program_sub['setNumber'] = setNumber
        self.program_sub['setName'] = setName
        self.program_sub['webUrl'] = webUrl
        self.program_sub['poster'] = poster
        self.program_sub['playLength'] = playLength
        self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = beauty_mmwu_1()
    app.doProcess()