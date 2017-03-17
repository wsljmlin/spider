#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderTool import spiderTool
from vipmediaContent import BASE_CONTENT
from vipmediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_iqiyi_vipreal():
    def __init__(self):
        print "Do spider all_iqiyi_vipreal."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.seedBase = ["http://list.iqiyi.com/www/3/----------2---4-1--iqiyi-1-.html"
                         , "http://list.iqiyi.com/www/3/----------2---4-1--iqiyi-1-.html"
                         , "http://list.iqiyi.com/www/3/----------2---4-2--iqiyi-1-.html"
                         , "http://list.iqiyi.com/www/3/----------2---4-3--iqiyi-1-.html"
                         , "http://list.iqiyi.com/www/3/----------2---4-4--iqiyi-1-.html"
                         , "http://list.iqiyi.com/www/3/----------2---4-5--iqiyi-1-.html"
                        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.seqNocnt = 1
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_iqiyi_vipreal_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("div", attrs={"class": "wrapper-piclist"})
            if seed_P is not None:
                seedList = seed_P.find_all("div", attrs={"class": "site-piclist_pic"})
            for each in seedList:
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        self.seedList.append(subSeed)
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "纪录片".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program["name"],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            # add seqnum
            self.program['seqNo'] = self.seqNocnt
            self.seqNocnt = self.seqNocnt + 1

            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        name = ""
        poster = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("img", attrs={'width': '195'})
        poster_p_1 = soup.find('div', attrs={'class': 'album-picCon album-picCon-onePic'})
        if poster_p is not None:
            poster = poster_p.get("src")
            name = poster_p.get("alt")
        elif poster_p_1 is not None:
            img_tag = poster_p_1.find("img")
            if img_tag is not None:
                poster = img_tag.get("src")
                name = img_tag.get("alt")

        detail = soup.find("div", attrs={"class": "result_detail-minH"})
        detail_1 = soup.find("div", attrs={"class": "msg-hd-lt fl"})
        if detail is not None:
            for div_p in detail.find_all("div", attrs={"class": "topic_item clearfix"}):
                for each in div_p.find_all("div"):
                    a_list = []
                    for a_tag in each.find_all('a'):
                        a_list.append(a_tag.get_text())
                    a_str = ",".join(a_list)
                    if re.search("主持人：".decode("utf8"),each.get_text()):
                        star = a_str
                    if re.search("类型：".decode("utf8"),each.get_text()):
                        ctype = a_str
                    if re.search("语言：".decode("utf8"),each.get_text()):
                        programLanguage = a_str
                    if re.search("地区：".decode("utf8"),each.get_text()):
                        area = a_str
        elif detail_1:
                for each in detail_1.find_all("p"):
                    a_list = []
                    for a_tag in each.find_all('a'):
                        a_list.append(a_tag.get_text())
                    a_str = ",".join(a_list)
                    if re.search("主持人：".decode("utf8"),each.get_text()):
                        star = a_str
                    if re.search("类型：".decode("utf8"),each.get_text()):
                        ctype = a_str
                    if re.search("语言：".decode("utf8"),each.get_text()):
                        programLanguage = a_str
                    if re.search("地区：".decode("utf8"),each.get_text()):
                        area = a_str

        content_p = soup.find('span',  attrs={"class": "showMoreText", "data-moreorless":"moreinfo", "style":"display: none;"})
        content_p_1 = soup.find("span", attrs={"class": "bigPic-b-jtxt"})
        if content_p is not None:
            if content_p.find("span"):
                content_p = content_p.find("span")
            if re.search("简介：".decode("utf8"),content_p.get_text()):
                intro = content_p.get_text().split("简介：".decode("utf8"))[1].strip()
        elif content_p_1 is not None:
            intro = content_p_1.get_text()

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro

        sourceId = "0"
        seed_P = re.search(r'sourceId:\s*(?P<sourceId>\d+),\s+cid:\s*(?P<cid>\d+)', doc)
        seed_P1 = re.search(r'albumId:\s*(?P<albumId>\d+)', doc)
        if seed_P:
            sourceId = seed_P.group('sourceId')
            cid = seed_P.group('cid')
            self.program['mainId'] = sourceId
            seed_sub = 'http://cache.video.iqiyi.com/jp/sdvlst/%s/%s/' %(cid,sourceId)
            if sourceId != '0':
                self.secondSpider(seed_sub)
        if sourceId == '0' and seed_P1:
            albumId = seed_P1.group('albumId')
            self.program['mainId'] =  albumId
            seed_sub = 'http://cache.video.iqiyi.com/jp/avlist/%s/' %(albumId)
            allNum = 0
            doc = spiderTool.getHtmlBody(seed_sub)
            try:
                json_data = json.loads(doc.split('=')[1])
                data = json_data["data"]["vlist"]
                allNum = json_data["data"]["allNum"]
            except:
                data = []
            for i in range(1,(int(allNum)/50 + 2)):
                seed_sub = 'http://cache.video.iqiyi.com/jp/avlist/%s/%s/50/' %(albumId, str(i))
                self.secondSpider1(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc.split('=')[1])
            data = json_data["data"]
        except:
            data = []
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = each['tvYear']
            setName = each['videoName']
            webUrl = each['vUrl']
            poster = each['aPicUrl']
            playLength = each['timeLength']
            setIntro = each['desc']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = str(int(playLength)/60) + ':' + str(int(playLength)%60)
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

    def secondSpider1(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc.split('=')[1])
            data = json_data["data"]["vlist"]
        except:
            data = []
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = str(each['pd'])
            setName = each['vn']
            webUrl = each['vurl']
            poster = each['vpic']
            playLength = each['timeLength']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = str(int(playLength)/60) + ':' + str(int(playLength)%60)
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_iqiyi_vipreal()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()