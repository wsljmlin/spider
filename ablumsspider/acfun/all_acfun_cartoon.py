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

class all_acfun_cartoon():
    def __init__(self):
        self.base=["http://www.acfun.tv/v/list144/index.htm#page=1"
                   ,"http://www.acfun.tv/v/list144/index.htm#page=1"
                   ,"http://www.acfun.tv/v/list144/index.htm#page=2"
                   ,"http://www.acfun.tv/v/list144/index.htm#page=3"
                   ,"http://www.acfun.tv/v/list144/index.htm#page=4"
                   ,"http://www.acfun.tv/v/list144/index.htm#page=5"
                   ]
        self.seedList = []
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_acfun_cartoon_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()


    def doProcess(self):
        for seed in self.base:
            self.seedList = []
            pageNo_p = seed.split('#')[1]
            pageNo_p = re.match(r'page=(\d+)',pageNo_p)
            pageNo = pageNo_p.group(1)
            seed_p = "http://www.acfun.tv/bangumi/bangumi/page?pageSize=42&isWeb=1&pageNo=%s&sort=1" % pageNo

            doc = spiderTool.getHtmlBody(seed_p)
            try:
                jsondata = json.loads(doc)
                jsondata = json.loads(doc)
            except:
                continue

            if not jsondata.get('data'):
                continue
            data = jsondata['data']['list']
            for each in data:
                if each.get('id')  is not None:
                    seed = "http://www.acfun.tv/v/ab%s" % each['id']
                    self.seedList.append(seed)
            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = 'ACFUN'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.firstSpider(seed)
            self.program['mainId'] = "ab%s" % self.program['mainId']
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program["name"],self.program['totalSets']

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
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
        playTimes = 0
        pcUrl = ""
        duration = ""
        alias = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        detailpage = soup.find('div', attrs={'class': 'details page'})
        if detailpage is not None:
            area_title = detailpage.find('div', attrs={'class': 'area-title'})
            if area_title is not None:
                name = area_title.find('h3').get_text()

            #get poster
            poster_p = detailpage.find('img', attrs={'class': 'cover'})
            if poster_p is not None:
                poster = poster_p.get('src')

            page_info = detailpage.find('div', attrs={'class': 'area-info'})
            if page_info is not None:
                #get ctype
                ctype_list = []
                ctype_p = page_info.find('div', attrs={'class': 'block-tag'}).find_all('a')
                if ctype_p is not None:
                    for atype in ctype_p:
                        ctype_list.append(atype.get_text())
                    ctype = ','.join(ctype_list)
                #get shootyear
                shootYear_p = page_info.find('div', attrs={'class': 'block-date'}).find('a')
                if shootYear_p is not None:
                    shootYear = shootYear_p.get_text()
                #get description
                intro_p = page_info.find('div', attrs={'class': 'block-desc'})
                if intro_p is not None:
                    intro = intro_p.get_text()

        if re.match(r'http://www\.acfun\.tv/v/ab(.*)', seed):
            mainId = re.match(r'http://www\.acfun\.tv/v/ab(.*)', seed).group(1)


        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url', poster)
        self.program['star'] = spiderTool.listStringToJson('name', star)
        self.program['director'] = spiderTool.listStringToJson('name', director)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        #get toltal Page
        sub_seedlist = []
        sub_seed = "http://www.acfun.tv/bangumi/video/page?bangumiId=%s&pageSize=30&pageNo=1&isWeb=1&order=2" % mainId
        doc = spiderTool.getHtmlBody(sub_seed)
        try:
            jsondata = json.loads(doc)
        except:
            return
        if not jsondata.get('data'):
            return
        toltalPage = jsondata['data']['totalPage']

        for index in range(toltalPage):
            sub_seed = "http://www.acfun.tv/bangumi/video/page?bangumiId=%s&pageSize=30&pageNo=%d&isWeb=1&order=2" % (mainId, index+1)
            self.secondSpider(sub_seed)



    def secondSpider(self, sub_seed):
        doc = spiderTool.getHtmlBody(sub_seed)
        try:
            jsondata=json.loads(doc)
        except:
            return
        if not jsondata.get('data'):
            return

        toltalCount = int(jsondata['data']['totalCount'])

        data = jsondata['data']['list']
        for item in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            setIntro = ""
            plot = []

            sortLoginc = item['sortLogic']
            setName = item['title']
            if re.search(r'(\d+)'.decode('utf-8'), setName):
                setNumber = re.search(r'(\d+)'.decode('utf-8'), setName).group(1)
            else:
                setNumber = str(toltalCount - int(sortLoginc) + 1)
            webUrl = "http://www.acfun.tv/v/ab%s_%s" % (self.program['mainId'], setNumber)

            if setNumber == "" or setName == "" or setNumber is None or setName is None or webUrl is None or webUrl == "" or \
                    re.search(r'预告'.decode('utf8'), setName):
                continue

            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_acfun_cartoon()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()


