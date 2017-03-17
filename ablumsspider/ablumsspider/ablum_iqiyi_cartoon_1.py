#!/usr/bin/env python
#encoding=UTF-8
import re
import json
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
#数码宝贝tri


class ablum_iqiyi_cartoon_1():
    def __init__(self):
        print "Do spider ablum_iqiyi_cartoon_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://www.iqiyi.com/lib/m_208711414.html", #数码宝贝tri
                         "http://www.iqiyi.com/lib/m_208711414.html", #数码宝贝tri
                         "http://www.iqiyi.com/lib/m_210306014.html" #魔法少女伊莉雅第4季
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_iqiyi_cartoon_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'], self.program['totalSets'], self.program['mainId']
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
        alias = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("div", attrs={'class': 'result_pic'})
        if poster_p is not None:
            poster = poster_p.find('img').get('src')

        name_p = soup.find('h1', attrs={'class': 'main_title'})
        if name_p is not None:
            name = name_p.find('a').get_text()
            if re.search(r'\d+.\.\d+', name_p.get_text()):
                point = float(re.search(r'\d+.\.\d+', name_p.get_text()).groups())


        detail = soup.find_all("div", attrs={"class": "topic_item clearfix"})
        for each in detail:
            if each.find('div', attrs={"class": "look_point"}):
                ctype_p = each.find('div', attrs={"class": "look_point"})
                a_list = []
                for a_tag in ctype_p.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                ctype = a_str

            for p_tag in each.find_all('em'):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("配音：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str



        content_p = soup.find('p',  attrs={"data-movlbshowmore-ele":"whole"})
        if content_p is not None:
            intro = content_p.get_text().strip()

        mainId_P = re.search(r'http://www\.iqiyi\.com/lib/(\w+)\.html', seed)
        if mainId_P:
            mainId = mainId_P.group(1)


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        self.secondSpider(doc)

    def secondSpider(self, doc):
        detail = re.findall(r'<li class="album_item">\s+<a data-pb=[^\\]*?href="(?P<url>.*?)"[^\\]*?title="(?P<num>.*?)"'.decode('utf8'), doc)
        for each in detail:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = each[1]
            setName = self.program['name']
            webUrl = each[0]
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = ablum_iqiyi_cartoon_1()
    app.doProcess()