#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import types
from spiderModel.spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
#最好我们


class all_pptv_variety():
    def __init__(self):
        print "Do spider all_pptv_variety."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.pptv.com/channel_list.html?type=4&page=1",
                         "http://list.pptv.com/channel_list.html?type=4&page=1"
                         "http://list.pptv.com/channel_list.html?type=4&page=2"
                         "http://list.pptv.com/channel_list.html?type=4&page=3"
                         "http://list.pptv.com/channel_list.html?type=4&page=4"
                         "http://list.pptv.com/channel_list.html?type=4&page=5"
                         "http://list.pptv.com/channel_list.html?type=4&page=6"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_pptv_variety_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seedSoup = soup.find_all('a', attrs={'class': 'ui-list-ct'})
            for each in seedSoup:
                    subSeed = each.get("href")
                    if subSeed is not None:
                        self.seedList.append(subSeed)
        self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)

            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = 'PPTV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            #print self.program["name"], self.program['totalSets']
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



        if re.search(r'http://v.pptv.com/show/\w+\.html', seed):
            seed_post = seed.replace("/show/", "/page/")
        else:
            seed_post = seed

        doc = spiderTool.getHtmlBody(seed_post)

        soup = BeautifulSoup(doc, from_encoding="utf8")
        poster_P = soup.find("a", attrs={"class": "cover-a"})
        poster_P1 = soup.find("div", attrs={"class": "bd cf"})
        if poster_P is not None:
            img_tag = poster_P.find("img")
            if img_tag is not None:
                img = img_tag.get('data-src2')
                if img is not None:
                    poster = img
        elif poster_P1 is not None:
            img_tag = poster_P1.find("img")
            if img_tag is not None:
                img = img_tag.get('src')
                if img is not None:
                    poster = img

        if re.search(r'http://v.pptv.com/page/\w+\.html', seed):
            seed = seed.replace("/page/", "/show/")
        doc = spiderTool.getHtmlBody(seed)



        pid_P = re.search(r'"pid":\s*(?P<pid>\d+),'.decode('utf8'), doc)
        if pid_P:
            pid = pid_P.group('pid')
            seed_sub = 'http://v.pptv.com/show/videoList?&cb=videoList&pid=' + pid
            mainId = pid
        else:
            return

        id_P = re.search(r'"id":\s*(?P<id>\d+),'.decode('utf8'), doc)
        if id_P:
            id = id_P.group('id')
            seed = 'http://svcdn.pptv.com/show/v1/meta.json?cid=%s&sid=%s&psize=50' % (id, pid)
        else:
            return

        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc)
        if json_data.has_key("data"):
            data = json_data["data"]
        else:
            return

        if data.has_key("set"):
            name_P = data["set"]
            if type(name_P) is types.ListType:
                if len(name_P) == 2:
                    name = name_P[0]
                    pcUrl = name_P[1]

        def getListName(dict_P):
            dict_list = []
            if type(dict_P) is types.ListType:
                for each in dict_P:
                    if type(each) is not types.DictionaryType:
                        continue
                    name = ""
                    if each.has_key("name"):
                        name = each["name"]
                    elif each.has_key("text"):
                        name = each["text"]
                    if re.search(r'未知'.decode('utf8'), name) or name == '':
                        continue
                    dict_list.append(name)
            return ",".join(dict_list)

        if data.has_key("directors"):
            star = getListName(data["directors"])

        if data.has_key("ct"):
            ctype = getListName(data["ct"])

        if data.has_key("area"):
            area = getListName(data["area"])

        if data.has_key("score"):
            point = data["score"]
        try:
            point = float(point)
        except:
            point = 0.0

        if data.has_key("summary"):
            intro = data["summary"]



        self.program["name"] = spiderTool.changeName(name)
        self.program['pcUrl'] = pcUrl
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['point'] = point
        self.program['mainId'] = mainId

        self.secondSpider(seed_sub)


    def secondSpider(self, seed):
        data = ""
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc.split('videoList(')[1][:-2])
        if type(json_data) is types.DictionaryType and json_data.has_key("data"):
            data_P = json_data["data"]
            if type(data_P) is types.DictionaryType and data_P.has_key("list"):
                data = data_P["list"]
        if type(data) is not types.ListType or data == "":
            return
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            if each.has_key("date"):
                setNumber = each['date']
            if each.has_key("title"):
                setName = each['title']
            if each.has_key("url"):
                webUrl = each['url']
            if each.has_key("capture"):
                poster = each['capture']
            if setNumber == "" and re.search(r'^\d{6}'.decode('utf8'), setName):
                setNumber = re.search(r'^\d{6}', setName).group()
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_pptv_variety()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()