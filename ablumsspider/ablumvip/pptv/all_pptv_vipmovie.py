#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import types
from spiderTool import spiderTool
from vipmediaContent import BASE_CONTENT
from vipmediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
from collections import OrderedDict



class all_pptv_vipmovie():
    def __init__(self):
        print "Do spider all_pptv_vipmovie."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=1"
                         , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=1"
                         , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=2"
                         , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=3"
                         , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=4"
                         , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=5"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=6"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=7"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=8"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=9"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=10"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=11"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=12"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=13"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=14"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=15"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=16"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=17"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=18"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=19"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=20"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=21"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=22"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=23"
                         # , "http://vip.pptv.com/newlist/lazyload1?mtype=all&mtime=&marea=&mneedpay=%E4%BC%9A%E5%91%98%E5%85%8D%E8%B4%B9&mkind=2&pagenum=24"
                     ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.prgdata = {}
        self.seqNocnt = 1
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_pptv_vipmovie_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            doc = spiderTool.getHtmlBody(seed)
            try:
                data = json.loads(doc, object_pairs_hook=OrderedDict)

            except:
                # print("load json error1111!")
                continue

            for key, value in data.iteritems():
                if value.get('url'):
                    subseed = value['url']
                    if re.search(r"http", subseed):
                        self.seedList.append(subseed)
                        if value.get('imgsrc'):
                            prgdata = {}
                            prgdata['poster'] = value['imgsrc']
                            self.prgdata[subseed] = prgdata

            self.seedSpider()


    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            # add poster
            if self.prgdata.get(seed):
                poster = self.prgdata[seed]['poster']
                self.program['poster'] = spiderTool.listStringToJson('url', poster)
            self.firstSpider(seed)
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = 'PPTV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            # print self.program["name"], self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            # add seqnum
            self.program['seqNo'] = self.seqNocnt
            self.seqNocnt = self.seqNocnt + 1

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        name = ""
        pcUrl = ""
        poster = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        point = ""
        mainId = ""
        area = ""
        shootYear = ""
        duration = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        #get name
        name_p = soup.find('div', attrs={'class': 'title_video'})
        if name_p is not None:
            if name_p.find('h3') is not None:
                name = name_p.find('h3').get_text()

        #get point
        point_p = soup.find('div', attrs={'class' : 'scoremark scores'})
        if point_p is not None:
            if point_p.find('em') is not None:
                point = point_p.find('em').get_text()

        #
        infolist = soup.find("div", attrs={"class": "intro-content intro-short"})
        if infolist is not None:
            li_list = infolist.find_all('li')
            for li in li_list:
                li_p = str(li)

                if re.search(r'.*主演.*'.decode('utf8'), li_p.decode('utf8')):
                    star_list = []
                    star_p = li.find_all('a')
                    for each in star_p:
                        star_list.append(each.get_text())
                    star = ','.join(star_list)
                elif re.search(r'.*地区.*'.decode('utf8'), li_p.decode('utf8')):
                    area_p = li.get_text()
                    area_p = re.findall(r'地区：(.*)'.decode('utf8'), area_p)
                    if area_p:
                        area = area_p[0]
                        area = area.replace('/', ',')
                elif re.search(r'.*导演.*'.decode('utf8'), li_p.decode('utf8')):
                    director_p = li.find('a')
                    if director_p is not None:
                        director = director_p.get_text()
                elif re.search(r'.*类型.*'.decode('utf8'), li_p.decode('utf8')):
                    type_p = li.find_all('a')
                    type_list = []
                    for each in type_p:
                        type_list.append(each.get_text())
                    ctype = ','.join(type_list)
                elif re.search(r'.*上映.*'.decode('utf8'), li_p.decode('utf8')):
                    shootYear_p = li.get_text()
                    shootYear_p = re.search(r'\d+', shootYear_p)
                    if shootYear_p is not None:
                        shootYear = shootYear_p.group(0)
                elif re.search(r'.*片长.*'.decode('utf8'), li_p.decode('utf8')):
                    duration_p = li.get_text()
                    duration_p = re.search(r'\d+', duration_p)
                    if duration_p is not None:
                        duration = duration_p.group(0)

            intro_p = infolist.find('p', attrs={'class': 'longinfo'})
            if intro_p is not None:
                intro = intro_p.get_text().strip()

        if re.match(r'http://ddp\.vip\.pptv\.com/play/(.*).html', seed):
            mainId = re.match(r'http://ddp\.vip\.pptv\.com/play/(.*).html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['pcUrl'] = seed
        # self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['point'] = point
        self.program['mainId'] = mainId

        self.secondSpider()


    def secondSpider(self):
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = "1"
            setName = self.program['name']
            webUrl = self.program['pcUrl']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                return
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            if len(self.program['poster']) > 0:
                self.program_sub['poster'] = self.program['poster'][0]['url']
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_pptv_vipmovie()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
