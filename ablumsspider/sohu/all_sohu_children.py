#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import codecs
import urllib
import base64
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_sohu_children():
    def __init__(self):
        print "Do spider all_sohu_cartoon."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p61_p73_p8_p9_p101_p11_p12_p13.html" #0-3
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p61_p73_p8_p9_p101_p11_p12_p13.html" #0-3
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p61_p73_p8_p9_p102_p11_p12_p13.html" #0-3
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p61_p73_p8_p9_p103_p11_p12_p13.html" #0-3
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p62_p73_p8_p9_p101_p11_p12_p13.html" #4-6
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p62_p73_p8_p9_p102_p11_p12_p13.html" #4-6
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p62_p73_p8_p9_p103_p11_p12_p13.html" #4-6
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p63_p73_p8_p9_p101_p11_p12_p13.html" #7-9
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p63_p73_p8_p9_p102_p11_p12_p13.html" #7-9
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p63_p73_p8_p9_p103_p11_p12_p13.html" #7-9
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p64_p73_p8_p9_p101_p11_p12_p13.html" #10-12
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p64_p73_p8_p9_p102_p11_p12_p13.html" #10-12
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p64_p73_p8_p9_p103_p11_p12_p13.html" #10-12
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p65_p73_p8_p9_p101_p11_p12_p13.html" #13-17
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p65_p73_p8_p9_p102_p11_p12_p13.html" #13-17
                       , "http://so.tv.sohu.com/list_p1115_p2_p3_p4_p5_p65_p73_p8_p9_p103_p11_p12_p13.html" #13-17
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_sohu_children_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("ul", attrs={"class": "st-list cfix"})
            if seed_P is not None:
                seedList = seed_P.find_all("li")
            for each in seedList:
                a_tag = each.find("a", attrs={"target": "_blank"})
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        subSeed = "http:%s" % subSeed
                        self.seedList.append(subSeed)
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = '搜狐'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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
        point = 0.0
        poster = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        mainId = ""

        doc = spiderTool.getHtmlBody(seed)
        if re.search(r'playlistId\s*=\s*"(\d+)"', doc):
            mainId = re.search(r'playlistId\s*=\s*"(\d+)"', doc).group(1)
        elif re.search(r'PLAYLIST_ID\s*=\s*"(\d+)"', doc):
            mainId = re.search(r'PLAYLIST_ID\s*=\s*"(\d+)"', doc).group(1)
        elif re.search(r'http://film\.sohu\.com/album/(\d+)\.html', seed):
            mainId = re.search(r'http://film\.sohu\.com/album/(\d+)\.html', seed).group(1)
        else:
            return

        seed = "http://pl.hd.sohu.com/videolist?playlistid=%s&callback=__get_videolist" %(mainId)
        try:
            doc = spiderTool.getHtmlBody(seed).decode('gbk').encode('utf8')
            doc = doc.split('__get_videolist(')[1][:-2]
            data = json.loads(doc)
        except:
            return

        if data.has_key('albumName'):
            name = data['albumName']
        if data.has_key('mainActors'):
            star = ','.join(data['mainActors'])
        if data.has_key('categories'):
            ctype = ','.join(data['categories'])
        if data.has_key('publishYear'):
            shootYear = str(data['publishYear'])
        if data.has_key('albumDesc'):
            intro = data['albumDesc']
        if data.has_key('largeVerPicUrl'):
            poster = data['largeVerPicUrl']
        if data.has_key('directors'):
            director = ','.join(data['directors'])
        if data.has_key('area'):
            area = data['area']

        self.program["name"] = spiderTool.changeName(name)
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
        self.program['mainId'] = mainId

        if data.has_key('videos'):
            videos = data['videos']
            self.secondSpider(videos)


    def secondSpider(self, videos):
        for each in videos:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""

            if each.has_key('name'):
                setName = each['name']
            if each.has_key('pageUrl'):
                webUrl = each['pageUrl']
            if each.has_key('order'):
                setNumber = each['order']
            if each.has_key('largePicUrl'):
                poster = each['largePicUrl']

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_sohu_children()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()