#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import types
import os
import time
import copy
from spiderModel.spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_mgtv_real():
    def __init__(self):
        print "Do spider all_mgtv_real."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.mgtv.com/5/---------5-1---.html"
                         , "http://list.mgtv.com/5/---------5-2---.html"
                         , "http://list.mgtv.com/5/---------5-3---.html"
                         , "http://list.mgtv.com/5/---------5-4---.html"
                         , "http://list.mgtv.com/5/---------5-5---.html"
                         , "http://list.mgtv.com/5/---------5-6---.html"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_mgtv_real_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("ul", attrs={"class": "clearfix ullist-ele"})
            if seed_P is not None:
                seedList = seed_P.find_all("p", attrs={"class": "img-box"})
            for each in seedList:
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        subSeed = subSeed.replace('www.hunantv.com', 'www.mgtv.com')
                        self.seedList.append(subSeed)
        self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "纪录片".decode("utf8")
            self.program['website'] = '芒果TV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            #print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.jsonData = str + '\n'
            #self.dataFile.write(str + '\n')


    def firstSpider(self, seed):
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

        pid = ""
        pid_P = re.search(r'http://www.mgtv.com/\w/\d+/(?P<mainId>\d+)/\w/(?P<pid>\d+)\.html', seed)
        if pid_P:
            pid = pid_P.group('pid')
            mainId = pid_P.group('mainId')

        seedJson = ""
        if pid != '':
            seedJson = 'http://m.api.hunantv.com/video/getbyid?videoId=%s' %(pid)
        else:
            return
        if mainId == "":
            mainId = pid

        doc = spiderTool.getHtmlBody(seedJson)
        if re.search(r'<html>', doc):
            doc = spiderTool.getHtmlBody(seedJson)
        json_data = json.loads(doc.strip())

        if json_data.has_key("data"):
            if type(json_data["data"]) is types.DictionaryType:
                json_data = json_data["data"]
                if json_data.has_key("detail"):
                    json_data = json_data["detail"]
                else:
                    return
            else:
                return

        if json_data.has_key("collectionName"):
            name = json_data["collectionName"]

        if json_data.has_key("image"):
            poster = json_data["image"]

        if json_data.has_key("year"):
            shootYear = json_data["year"]

        if json_data.has_key("director"):
            director_P = json_data["director"]
            if type(director_P) is types.UnicodeType:
                director = director_P.strip().replace(" / ",",")

        if json_data.has_key("player"):
            star_P = json_data["player"]
            if type(star_P) is types.UnicodeType:
                star = star_P.strip().replace(" / ",",")

        if json_data.has_key("area"):
            area_P = json_data["area"]
            if type(area_P) is types.UnicodeType:
                area = area_P.strip().replace(" ",",")

        if json_data.has_key('desc'):
            intro = json_data['desc']


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

        if json_data.has_key('typeId'):
            typeId = json_data['typeId']
        if json_data.has_key('collectionId'):
            collectionId = json_data['collectionId']

        pageNum = 20
        if json_data.has_key("totalvideocount"):
            pageNum = json_data["totalvideocount"]
        seed_sub = "http://m.api.hunantv.com/video/getListV2?videoId=%s&pageId=0&pageNum=%s"  %(pid, pageNum)
        try:
            self.secondSpider(seed_sub, seed, pid)
        except:
            print "spider error: " + seed
    def secondSpider(self, seed, seed_P, pid):
        data = []
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc)
        if json_data is not None:
            if json_data.has_key('data'):
                data_p = json_data['data']
                if type(data_p) is types.DictionaryType:
                    if data_p.has_key('list'):
                        data = data_p['list']
        if type(data) is not types.ListType:
            return

        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''
            playLength = ""
            setIntro = ""
            if type(each) is not types.DictionaryType:
                return
            if each.has_key('videoId'):
                videoId = str(each['videoId'])
                webUrl = seed_P.replace(pid, videoId)

            if each.has_key('videoIndex'):
                setNumber = str(each['videoIndex'])
            if setNumber == "" and len(data) == 1:
                setNumber = '1'
            if each.has_key('name'):
                setName = each['name']

            if each.has_key('image'):
                poster = each['image']

            if each.has_key('desc'):
                setIntro = each['desc']

            if each.has_key('time'):
                timeLength = each['time'].encode('utf8')
                playLength = str(int(timeLength) / 60) + ":" + str(int(timeLength) % 60)

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_mgtv_real()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()