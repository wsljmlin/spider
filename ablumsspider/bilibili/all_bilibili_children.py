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

class all_bilibili_children():
    def __init__(self):
        self.base=["http://bangumi.bilibili.com/anime/index#p=1&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
                   ,"http://bangumi.bilibili.com/anime/index#p=1&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
                   ,"http://bangumi.bilibili.com/anime/index#p=2&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
                   ,"http://bangumi.bilibili.com/anime/index#p=3&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
                   ,"http://bangumi.bilibili.com/anime/index#p=4&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
                   ,"http://bangumi.bilibili.com/anime/index#p=5&v=0&area=&stat=0&y=0&q=0&tag=24&t=0&sort=0"
            ]
        self.seedList = []
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_bilibili_children_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()


    def doProcess(self):
        for seed in self.base:
            self.seedList = []
            pageNo_p = re.match(r'.*p=(\d+).*', seed)
            pageNo = pageNo_p.group(1)
            seed_p = "http://bangumi.bilibili.com/web_api/season/index?page=%s&page_size=20&version=0&is_finish=0&start_year=0&quarter=0&tag_id=24&index_type=0&index_sort=0" % pageNo
            doc = spiderTool.getHtmlBody(seed_p)
            try:
                jsondata = json.loads(doc)
            except:
                continue

            if not jsondata.get('result'):
                continue
            data = jsondata['result']['list']

            for each in data:
                if each.get('url') is not None:
                    sub_seed = each['url']
                    self.seedList.append(sub_seed)
            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.program["ptype"] = "少儿".decode("utf8")
            self.program['website'] = 'bilibili'.decode("utf8")
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
        introPage = soup.find('div', attrs={'class': 'info-content'})
        if introPage is not None:
            #get poster
            poster_p = introPage.find('div', attrs={'class': 'bangumi-preview'})
            if poster_p is not None:
                poster = poster_p.find('img').get('src')
                if not re.match(r'http://', poster):
                    poster = "http:%s" % poster

            #get info
            info_p = introPage.find('div', attrs={'class': 'bangumi-info-r'})
            if info_p is not None:
                head = info_p.find('div', attrs={'class': 'b-head'})
                if head is not None:
                    # get name
                    name = head.find('h1').get_text()

                    #get ctype
                    ctype_list = []
                    ctype_p = head.find_all('span')
                    for span in ctype_p:
                        ctype_list.append(span.get_text())
                    ctype = ','.join(ctype_list)

                #get playtimes
                info_count = info_p.find('div', attrs={'class': 'info-count'})
                if info_count is not None:
                    #playTimes = info_count.find('em').get_text()
                    playTimes = 0

                #get actors

                #get desc
                info_desc = info_p.find('div', attrs={'class': 'info-desc'})
                if info_desc is not None:
                    intro = info_desc.get_text().strip()


        if re.match(r'http://bangumi\.bilibili\.com/anime/(.*)', seed):
            mainId = re.match(r'http://bangumi\.bilibili\.com/anime/(.*)', seed).group(1)

        self.program['name'] = spiderTool.changeName(name)
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

        videoList = []
        subprg_list = soup.find_all('li', attrs={'class': 'v1-bangumi-list-part-child'})
        for li in subprg_list:
            if li.find('a').get('class') == ['v1-complete-text']:
                videoList.append(li)

        self.secondSpider(videoList)


    def secondSpider(self, videolist):
        for each in videolist:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""

            webUrl = each.find('a',attrs={'class': 'v1-complete-text'}).get('href')
            if not re.match(r'http://', webUrl):
                webUrl = "http:%s" % webUrl
            setName = each.find('a',attrs={'class': 'v1-complete-text'}).get('title')
            poster = each.find('img').get('src')
            if not re.match(r'http://', poster):
                poster = "http:%s" % poster
            setNumber_p = re.search(r'第(.*)话'.decode('utf8'), setName)
            if setNumber_p:
                setNumber = setNumber_p.group(1)
            else:
                setNumber = 0

            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_bilibili_children()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()


