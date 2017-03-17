#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import types
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_le_news():
    def __init__(self):
        print "Do spider all_le_news."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=1&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=1&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=2&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=3&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=4&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=5&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=6&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=8&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=9&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=10&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=11&st=",
                         "http://list.le.com/apin/chandata.json?c=1009&d=2&o=1&p=12&st=",
        ]
        self.pidList = {}
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_le_news_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            try:
                json_data = json.loads(doc)
            except:
                json_data = {}
            if json_data.has_key("video_list"):
                if type(json_data["video_list"]) is types.ListType:
                    seedList = json_data["video_list"]
            for each in seedList:
                pid = ""
                vid = ""
                subSeed = ""
                if each.has_key("aid"):
                    if type(each["aid"]) is types.UnicodeType:
                        pid = each["aid"]
                        if self.pidList.has_key(pid):
                            pass
                        else:
                            self.pidList[pid] = []

                if pid != "" and each.has_key("vid"):
                    if type(each["vid"]) is types.UnicodeType:
                        vid = each["vid"]
                        subSeed = "http://www.le.com/ptv/vplay/" + vid + ".html"
                        self.pidList[pid].append(vid)

                if pid != "" and vid != "" and subSeed != "":
                    self.seedSpider(pid, vid, each)

    def seedSpider(self, pid, vid, detail):
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(pid, vid, detail)
            self.program['pcUrl'] = "http://www.le.com/ptv/vplay/" + vid + ".html"
            self.program["ptype"] = "新闻".decode("utf8")
            self.program['website'] = '乐视'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                return

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, pid, vid, detail):
        name = ""
        poster = ""
        point = 0.0
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""


        mainSeed = 'http://static.app.m.letv.com/android/mod/mob/ctl/album/act/detail/id/%s/pcode/010110014/version/5.2.3.mindex.html' %(pid)
        mainId = pid
        doc = spiderTool.getHtmlBody(mainSeed)
        try:
            json_data = json.loads(doc)
        except:
            json_data = {}
        if json_data.has_key("body"):
            if type(json_data["body"]) is types.DictionaryType:
                json_data = json_data["body"]
            else:
                return

        if json_data.has_key("nameCn"):
            name = json_data["nameCn"]

        if json_data.has_key("nameCn"):
            name = json_data["nameCn"]
        if json_data.has_key("picCollections"):
            poster_dict = json_data["picCollections"]
            if type(poster_dict) is types.DictionaryType:
                if poster_dict.has_key('150*200'):
                    poster = poster_dict['150*200']
                if poster == "":
                    for each in poster_dict:
                        if poster_dict[each] != "":
                            poster = poster_dict[each]

        if json_data.has_key("score"):
            try:
                point = float(json_data["score"])
            except:
                point = 0.0

        if json_data.has_key("releaseDate"):
            shootYear_P = json_data["releaseDate"]
            if re.search(r'(\d{4})-\d{2}-\d{2}',shootYear_P):
                shootYear = re.search(r'(\d{4})-\d{2}-\d{2}',shootYear_P).group(1)
            elif re.search(r'^\d{4}$',shootYear_P):
                shootYear = shootYear_P

        if json_data.has_key("directory"):
            director_P = json_data["directory"]
            if type(director_P) is types.UnicodeType:
                director = director_P.strip().replace(" ",",")

        if json_data.has_key("starring"):
            star_P = json_data["starring"]
            if type(star_P) is types.UnicodeType:
                star = star_P.strip().replace(" ",",")

        if json_data.has_key("area"):
            area_P = json_data["area"]
            if type(area_P) is types.UnicodeType:
                area = area_P.strip().replace(" ",",")

        if json_data.has_key("subCategory"):
            ctype_P = json_data["subCategory"]
            if type(ctype_P) is types.UnicodeType:
                ctype = ctype_P.strip().replace(" ",",")

        if json_data.has_key('description'):
            intro = json_data['description']

        if json_data.has_key('language'):
            programLanguage = json_data['language']


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['point'] = point
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        self.secondSpider(pid, vid, detail)
    def secondSpider(self, pid, vid, detail):
            each = detail
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''
            dateTime = time.strftime('%y%m%d',time.localtime(time.time()))
            if type(each) is not types.DictionaryType:
                return
            if self.pidList.has_key(pid):
                Number = len(self.pidList[pid]) + 1
                if Number < 10:
                    setNumber = dateTime + "00" + str(Number)
                elif Number <100:
                    setNumber = dateTime + "0" + str(Number)
                else:
                    setNumber = dateTime + str(Number)

            if each.has_key('name'):
                setName = each['name']

            if each.has_key('images'):
                poster_P = each['images']
                if type(poster_P) is types.DictionaryType:
                    if poster_P.has_key("150*200"):
                        poster = poster_P["150*200"]
            if vid != "":
                webUrl = 'http://www.le.com/ptv/vplay/%s.html' %(vid)
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                return
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_le_news()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()