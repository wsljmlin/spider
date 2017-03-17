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
#最好我们


class all_iqiyi_children():
    def __init__(self):
        print "Do spider all_iqiyi_children."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.iqiyi.com/www/4/---304----------4-1-1-iqiyi--.html"
                         ,"http://list.iqiyi.com/www/4/---304----------4-1-1-iqiyi--.html"  #0-3
                         ,"http://list.iqiyi.com/www/4/---304----------4-2-1-iqiyi--.html"  #0-3
                         ,"http://list.iqiyi.com/www/4/---1283----------4-1-1-iqiyi--.html"  #4-6
                         ,"http://list.iqiyi.com/www/4/---1283----------4-2-1-iqiyi--.html"  # 4-6
                         ,"http://list.iqiyi.com/www/4/---305----------4-1-1-iqiyi--.html"  #7-13
                         ,"http://list.iqiyi.com/www/4/---305----------4-2-1-iqiyi--.html"  # 7-13
                         ,"http://list.iqiyi.com/www/4/---306----------4-1-1-iqiyi--.html" # 14-17
                         ,"http://list.iqiyi.com/www/4/---306----------4-2-1-iqiyi--.html" # 14-17
                         ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_iqiyi_children_" + self.today + ".txt")

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
            self.program["ptype"] = "少儿".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'], self.program['totalSets']
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
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("ul", attrs={'class': 'focus_img_list'})
        poster_p_1 = soup.find("div", attrs={"class": "result_pic pr"})
        if poster_p is not None:
            poster_p_sub = poster_p.find('li').get('style')
            if re.search(r'\((.*?)\)'.decode('utf8'), poster_p_sub):
                poster = re.search(r'\((.*?)\)'.decode('utf8'), poster_p_sub).group(1)
        elif poster_p_1 is not None:
            img_tag = poster_p_1.find("img")
            if img_tag is not None:
                poster = img_tag.get("src")
                name = img_tag.get("alt")

        name_p = soup.find('a', attrs={'class': 'white'})
        if name_p is not None:
            name = name_p.get_text()

        detail = soup.find("div", attrs={"class": "result_detail-minH"})
        detail_1 = soup.find("div", attrs={"class": "msg-hd-lt fl"})
        if detail is not None:
            for div_p in detail.find_all("div", attrs={"class": "topic_item clearfix"}):
                for each in div_p.find_all("div"):
                    a_list = []
                    for a_tag in each.find_all('a'):
                        a_list.append(a_tag.get_text())
                    a_str = ",".join(a_list)
                    if re.search("主演：".decode("utf8"),each.get_text()):
                        star = a_str
                    if re.search("导演：".decode("utf8"),each.get_text()):
                        director = a_str
                    if re.search("类型：".decode("utf8"),each.get_text()):
                        ctype = a_str
                    if re.search("语言：".decode("utf8"),each.get_text()):
                        programLanguage = a_str
                    if re.search("地区：".decode("utf8"),each.get_text()):
                        area = a_str
        elif detail_1 is not None:
            for p_tag in detail_1.find_all("p"):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str

        content_p = soup.find('span',  attrs={"class": "showMoreText", "data-moreorless":"moreinfo", "style":"display: none;"})
        content_p_1 = soup.find('div',  attrs={"data-moreorless":"moreinfo"})
        if content_p is not None:
            if content_p.find("span"):
                content_p = content_p.find("span")
            if re.search("简介：".decode("utf8"),content_p.get_text()):
                intro = content_p.get_text().split("简介：".decode("utf8"))[1].strip()
        elif content_p_1 is not None:
            if re.search("简介：".decode("utf8"),content_p_1.get_text()):
                intro = content_p_1.get_text().split("简介：".decode("utf8"))[1].strip()


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro

        seed_P = re.search(r'albumId:\s*(?P<albumId>\d+)[^\\]*?cid:\s*(?P<cid>\d+)'.decode('utf8'), doc)
        if seed_P:
            albumId = seed_P.group('albumId')
            cid = seed_P.group('cid')
            self.program['mainId'] = cid + "_" +albumId
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
                self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc.split('=')[1])
            data = json_data["data"]["vlist"]
        except:
            data = []
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = each['pds']
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
    app = all_iqiyi_children()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
