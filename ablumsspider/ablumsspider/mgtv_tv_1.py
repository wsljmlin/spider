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


class mgtv_tv_1():
    def __init__(self):
        print "Do spider mgtv_tv_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://www.mgtv.com/v/2/293140/f/3268985.html",
                         "http://www.mgtv.com/v/2/291796/f/3293835.html", #半妖倾城
                         "http://www.mgtv.com/v/2/294337/f/3316605.html",#神犬小七
                         "http://www.mgtv.com/v/2/293050/f/3321343.html",#旋风少女第二季 第2集
                         "http://www.mgtv.com/v/2/104817/f/3590159.html",#青云志
                         ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "mgtv_tv_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '芒果TV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
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
        self.secondSpider(seed_sub, seed, pid)
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
    app = mgtv_tv_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()