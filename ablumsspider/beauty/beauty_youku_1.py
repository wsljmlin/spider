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


class beauty_youku_1():
    def __init__(self):
        print "Do spider beauty_youku_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = [ 'http://www.soku.com/search_video/q_%E7%BE%8E%E5%A5%B3%E5%86%99%E7%9C%9F_limitdate_0?site=14&_lg=10&orderby=2&spm=0.0.0.0.nfPeVF'#美女写真
                          ,'http://www.soku.com/search_video/q_%E7%BE%8E%E5%A5%B3%E5%86%99%E7%9C%9F_limitdate_0?site=14&_lg=10&orderby=2&spm=0.0.0.0.nfPeVF'#美女写真
                         ,'http://www.soku.com/search_video/q_%E7%BE%8E%E5%A5%B3%E7%83%AD%E8%88%9E_limitdate_0?site=14&_lg=10&orderby=2&spm=0.0.0.0.NziPkR'#美女热舞
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "beauty_youku_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            self.seedList = soup.find_all('div', attrs={'class': 'v', 'data-type': 'tipHandle'})
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
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
        poster_p = soup.find("div",attrs={'class':'v-thumb'})
        if poster_p is not None:
            if poster_p.find('img') is not None:
                poster = poster_p.find("img").get("src")
                name = poster_p.find("img").get("alt")
            if poster_p.find('span', attrs={'class': 'v-time'}):
                playLength = poster_p.find('span', attrs={'class': 'v-time'}).get_text()

        pcUrl_p = soup.find('div', attrs={'class': 'v-link'})
        if pcUrl_p is not None:
            atag = pcUrl_p.find('a')
            if atag is not None:
                pcUrl = atag.get('href')
        mainId_p = re.search(r'http://v.youku.com/v_show/(.*?)\.html', pcUrl)
        if mainId_p:
            mainId = mainId_p.group(1)

        setNum_p = soup.find('span', attrs={'class': 'r'})
        if setNum_p is not None:
            setNum_text = setNum_p.get_text()
            if re.search(r'(\d+)分钟前'.decode('utf8'), setNum_text):
                setNum = time.strftime('%Y%m%d',time.localtime(time.time()))
            elif re.search(r'\d+小时前'.decode('utf8'), setNum_text):
                setNum = time.strftime('%Y%m%d',time.localtime(time.time()))

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
        self.secondSpider(setNum, name, pcUrl, playLength, poster)

    def secondSpider(self, setNumber, setName, webUrl, playLength, poster):
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
    app = beauty_youku_1()
    app.doProcess()