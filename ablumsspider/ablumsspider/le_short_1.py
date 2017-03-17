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


class le_short_1():
    def __init__(self):
        print "Do spider le_short_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://www.le.com/ptv/vplay/24794432.html"]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "le_short_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "段视频".decode("utf8")
            self.program['website'] = '乐视'.decode("utf8")
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
        doc = spiderTool.getHtmlBody(seed)
        pid_P = re.search(r'pid:\s*(?P<pid>\d+),', doc)
        pid_P1 = re.search(r'pid:\s*"(?P<pid>\d+)"', doc)
        if pid_P:
            pid = pid_P.group('pid')
        elif pid_P1:
            pid = pid_P1.group('pid')
        else:
            print "not pid"

        if pid == "" or pid == "0":
            soup = BeautifulSoup(doc, from_encoding="utf8")
            more_tag = soup.find("a", attrs={'class': 'more'})
            if more_tag is not None:
                url = more_tag.get('href')
                if url is not None:
                    if re.search(r'http://www\.le\.com/tv/(?P<pid>\d+)\.html,',doc):
                        pid = re.search(r'http://www\.le\.com/tv/(?P<pid>\d+)\.html,',doc).group('pid')

        if pid != '' or pid != '0':
            seed = 'http://static.app.m.letv.com/android/mod/mob/ctl/album/act/detail/id/%s/pcode/010110014/version/5.2.3.mindex.html' %(pid)
        else:
            return

        mainId = pid
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc)
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
        print seed
        data = []
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc)
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
            if setName == '' and  each.has_key('nameCn'):
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
    app = le_short_1()
    app.doProcess()