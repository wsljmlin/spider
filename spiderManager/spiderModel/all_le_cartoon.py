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


class all_le_cartoon():
    def __init__(self):
        print "Do spider all_le_cartoon."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=1&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=1&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=2&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=3&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=4&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=5&s=1",
                         "http://list.le.com/apin/chandata.json?c=5&d=1&md=&o=20&p=6&s=1",
        ]
        self.seedList = []
        self.images = {}
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_le_cartoon_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            try:
                json_data = json.loads(doc)
            except:
                json_data = {}
            if json_data.has_key("album_list"):
                if type(json_data["album_list"]) is types.ListType:
                    seedList = json_data["album_list"]
            for each in seedList:
                pid = ""
                if each.has_key("aid"):
                    if type(each["aid"]) is types.UnicodeType:
                        pid = each["aid"]
                        subSeed = "http://www.le.com/comic/" + pid + ".html"
                        self.seedList.append(subSeed)
                if pid != "" and each.has_key("images"):
                    images = each["images"]
                    if type(images) is types.DictionaryType:
                        if images.has_key("600*800"):
                            self.images[pid] = images["600*800"]
        self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = '乐视'.decode("utf8")
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
        if re.search(r'http://www\.le\.com/comic/(?P<pid>\d+)\.html',seed):
            pid = re.search(r'http://www\.le\.com/comic/(?P<pid>\d+)\.html',seed).group('pid')
        elif re.search(r'http://www\.letv\.com/comic/(?P<pid>\d+)\.html',seed):
            pid = re.search(r'http://www\.letv\.com/comic/(?P<pid>\d+)\.html',seed).group('pid')
        if pid != '' or pid != '0':
            seed = 'http://static.app.m.letv.com/android/mod/mob/ctl/album/act/detail/id/%s/pcode/010110014/version/5.2.3.mindex.html' %(pid)
        else:
            return
        mainId = pid
        doc = spiderTool.getHtmlBody(seed)
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
                if poster_dict.has_key('400*300'):
                    poster = poster_dict['400*300']
                if poster == "":
                    for each in poster_dict:
                        if poster_dict[each] != "":
                            poster = poster_dict[each]
        if self.images.has_key(pid):
            poster = self.images[pid]

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

        seed_sub = "http://static.app.m.letv.com/android/mod/mob/ctl/videolist/act/detail/id/%s/vid/25520328/b/1/s/60/o/-1/m/0/pcode/010110014/version/5.2.3.mindex.html"  %(pid)
        self.secondSpider(seed_sub)
    def secondSpider(self, seed):
        data = []
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc)
        except:
            json_data = {}
        if json_data is not None:
            if json_data.has_key('body'):
                data_p = json_data['body']
                if type(data_p) is types.DictionaryType:
                    if data_p.has_key('videoInfo'):
                        data = data_p['videoInfo']
        if type(data) is not types.ListType:
            return
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''
            if type(each) is not types.DictionaryType:
                return
            if each.has_key('episode'):
                setNumber = each['episode']
            if setNumber == "" and len(data) == 1:
                setNumber = '1'
            if each.has_key('subTitle'):
                setName = each['subTitle']
            if setName == '' and each.has_key('nameCn'):
                setName = each['nameCn']
            if each.has_key('picAll'):
                poster_P = each['picAll']
                if type(poster_P) is types.DictionaryType:
                    for key in poster_P:
                        if type(poster_P[key]) is types.UnicodeType:
                            if poster_P[key] != '':
                                poster = poster_P[key]
                                break
            if each.has_key('id'):
                id = each['id']
                if type(id) is types.UnicodeType:
                    if id != '':
                        webUrl = 'http://www.le.com/ptv/vplay/%s.html' %(id)
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_le_cartoon()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()