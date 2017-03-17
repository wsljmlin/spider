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

class all_bilibili_movie():
    def __init__(self):
        self.base = [
                        {"http://www.bilibili.com/video/movie_west_1.html#!page=1":"145"} #欧美
                        ,{"http://www.bilibili.com/video/movie_west_1.html#!page=1":"145"} #欧美
                        ,{"http://www.bilibili.com/video/movie_japan_1.html!page=1":"146"} #日本
                        ,{"http://www.bilibili.com/video/movie_chinese_1.html!page=1":"147"} #国产
                        ,{"http://www.bilibili.com/video/movie-movie-1.html!page=1":"83"} #其它
        ]

        self.seedList = []
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_bilibili_movie_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()


    def doProcess(self):
        for seeddict in self.base:
            self.seedList = []
            key = seeddict.keys()[0];
            tid = seeddict[key]
            pageNo_p = re.search(r'page=(\d+)', key)
            pageNo = pageNo_p.group(1)
            seed_p = "http://api.bilibili.com/archive_rank/getarchiverankbypartion?&type=jsonp&tid=%s&pn=%s" % (tid, pageNo)

            doc = spiderTool.getHtmlBody(seed_p)
            try:
                jsondata = json.loads(doc)
            except:
                continue

            if not jsondata.get('data'):
                continue
            data = jsondata['data']['archives']
            datakeys =  data.keys()

            def numeric_compare(x, y):
                x = int(x)
                y = int(y)
                if x > y:
                    return 1
                elif x == y:
                    return 0
                else:  # x<y
                    return -1

            datakeys.sort(numeric_compare)
            for datakey in datakeys:
                sub_seed = "http://www.bilibili.com/video/av%s/" % data[datakey]['aid']
                self.seedList.append(sub_seed)
            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = 'bilibili'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.firstSpider(seed)
            self.program['totalSets'] = len(self.program['programSub'])
            #print self.program["name"], self.program['totalSets']

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == '' or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.jsonData = str + "\n"
            # self.dataFile.write(str + '\n')


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


        #get poster
        poster_p = soup.find('img', attrs={'class': 'cover_image'})
        if poster_p is not None:
            poster = poster_p.get('src')
            if not re.match(r'http://', poster):
                poster = "http:%s" % poster

        #get name
        page_body = soup.find('div', attrs={'class': 'b-page-body'})
        if page_body is not None:
            name_p = page_body.find('div', attrs={'class': 'v-title'})
            if name_p is not None:
                name = name_p.get_text()

        v_info = soup.find('div', attrs={'class': 'v_info'})
        if v_info is not None:
            #get intro
            intro_p = v_info.find('div', attrs={'class': 'intro'})
            if intro_p is not None:
                intro = intro_p.get_text().strip()

            #get ctype
            ctype_list = []
            ctype_p = v_info.find('div', attrs={'class': 's_tag'})
            if ctype_p is not None:
                ctype_p = ctype_p.find_all('li')
                for li in ctype_p:
                    ctype_list.append(li.get_text())
                ctype = ','.join(ctype_list)

        if re.match(r'http://www\.bilibili\.com/video/(.*)/', seed):
            mainId = re.match(r'http://www\.bilibili\.com/video/(.*)/', seed).group(1)

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

        self.program_sub['setNumber'] = setNumber
        self.program_sub['setName'] = setName
        self.program_sub['webUrl'] = webUrl
        self.program_sub['poster'] = poster
        self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_bilibili_movie()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()


