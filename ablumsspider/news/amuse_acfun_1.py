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

class amuse_acfun_1():
    def __init__(self):
        self.base=["http://www.acfun.tv/v/list86/index.htm#page=1" #生活娱乐
                    ,"http://www.acfun.tv/v/list86/index.htm#page=1" #生活娱乐
                    ,"http://www.acfun.tv/v/list87/index.htm#page=1" #鬼畜调教
                    ,"http://www.acfun.tv/v/list88/index.htm#page=1" #萌宠
                    ,"http://www.acfun.tv/v/list89/index.htm#page=1" #美食
                    #,"http://www.acfun.tv/v/list98/index.htm#page=1" #综艺
                    #,"http://www.acfun.tv/v/list174/index.htm#page=1" #娱乐直播
                   ]
        self.seedList = []
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "amuse_acfun_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()


    def doProcess(self):
        for seed in self.base:
            self.seedList = []
            pageNo_p = seed.split('#')[1]
            pageNo_p = re.match(r'page=(\d+)', pageNo_p)
            pageNo = pageNo_p.group(1)
            channelId_p = re.match(r'http://www.acfun.tv/v/list(\d+)/index.htm.*', seed)
            channelId = channelId_p.group(1)
            seed_p = "http://www.acfun.tv/list/getlist?channelId=%s&sort=0&pageSize=20&pageNo=%s" % (channelId, pageNo)

            doc = spiderTool.getHtmlBody(seed_p)
            try:
                jsondata = json.loads(doc)
            except:
                continue

            if not jsondata.get('data'):
                continue
            data = jsondata['data']['data']
            for each in data:
                if each.get('id') is not None:
                    sub_seed = "http://www.acfun.tv/v/ac%s" % each['id']
                    self.seedList.append(sub_seed)
            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.program["ptype"] = "娱乐".decode("utf8")
            self.program['website'] = 'ACFUN'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.firstSpider(seed)
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program["name"], self.program['totalSets']

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == '' or self.program['mainId'] is None \
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
        poster = ""
        playTimes = 0
        pcUrl = ""
        duration = ""
        alias = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        introPage = soup.find('div', attrs={'class': 'introduction'})

        pageInfo = soup.find('div', attrs={'id': 'pageInfo'})
        if pageInfo is not None:
            # name = pageInfo.get('data-title')
            poster = pageInfo.get('data-pic')
            # intro = pageInfo.get('data-desc')

        if introPage is not None:
            #get intro
            intro_p = introPage.find('div', attrs={'class': 'desc gheight'})
            if intro_p is not None:
                intro  = intro_p.find('div').get_text()

        #get platytimes
        playTimes_p = soup.find('section', attrs={'class': 'clearfix wp area crumb'})
        if playTimes_p is not None:
            #playTimes = long(playTimes_p.find('span', attrs={'class': 'sp2'}).get_text())
            playTimes = 0

        if re.match(r'http://www\.acfun\.tv/v/(.*)', seed):
            mainId = re.match(r'http://www\.acfun\.tv/v/(.*)', seed).group(1)

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

        videoList = []
        soup = BeautifulSoup(doc, from_encoding="utf8")
        data = soup.find_all('script')
        for li in data:
            if re.match(r'.*pageInfo.*', ''.join(li)):
                pageInfo = li.get_text()
                pageInfo_p = re.findall(r'pageInfo\s+=\s+(.*)', pageInfo)
                if pageInfo_p:
                    try:
                        pageInfo_json = json.loads(pageInfo_p[0])
                    except:
                        break;
                    #get ctype
                    ctype_list = []
                    for tag in pageInfo_json['tagList']:
                        ctype_list.append(tag['name'])
                    ctype = ','.join(ctype_list)
                    #get name
                    name = pageInfo_json['title']
                    videoList = pageInfo_json['videoList']

        self.program["name"] = spiderTool.changeName(name)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)

        self.secondSpider(videoList)


    def secondSpider(self, videolist):
        for each in videolist:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""

            webUrl = "%s_%d" % (self.program['pcUrl'], (each['index']+1))
            if len(videolist) > 1:
                setName = each['title']
            else:
                setName = self.program["name"]
            setNumber = str(each['index']+1)

            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = amuse_acfun_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()


