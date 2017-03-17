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



class iqiyi_movie_1():
    def __init__(self):
        print "Do spider iqiyi_movie_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = [
"http://www.iqiyi.com/lib/m_209637714.html",
"http://www.iqiyi.com/lib/m_209626614.html",
"http://www.iqiyi.com/lib/m_209591514.html",
"http://www.iqiyi.com/lib/m_209502114.html",
"http://www.iqiyi.com/lib/m_209501414.html",
"http://www.iqiyi.com/lib/m_209467714.html",
"http://www.iqiyi.com/lib/m_209461514.html",
"http://www.iqiyi.com/lib/m_209377414.html",
"http://www.iqiyi.com/lib/m_209311014.html",
"http://www.iqiyi.com/lib/m_209222714.html",
"http://www.iqiyi.com/lib/m_209215514.html",
"http://www.iqiyi.com/lib/m_209172414.html",
"http://www.iqiyi.com/lib/m_209085214.html",
"http://www.iqiyi.com/lib/m_209046414.html",
"http://www.iqiyi.com/lib/m_209008914.html",
"http://www.iqiyi.com/lib/m_208972514.html",
"http://www.iqiyi.com/lib/m_208935614.html",
"http://www.iqiyi.com/lib/m_208907614.html",
"http://www.iqiyi.com/lib/m_208907614.html",
"http://www.iqiyi.com/lib/m_208871114.html",
"http://www.iqiyi.com/lib/m_208870714.html",
"http://www.iqiyi.com/lib/m_208814014.html",
"http://www.iqiyi.com/lib/m_208785714.html",
"http://www.iqiyi.com/lib/m_208785714.html",
"http://www.iqiyi.com/lib/m_208703014.html",
"http://www.iqiyi.com/lib/m_208683914.html",
"http://www.iqiyi.com/lib/m_208670314.html",
"http://www.iqiyi.com/lib/m_208667814.html",
"http://www.iqiyi.com/lib/m_208592014.html",
"http://www.iqiyi.com/lib/m_208589914.html",
"http://www.iqiyi.com/lib/m_208585114.html",
"http://www.iqiyi.com/lib/m_208532914.html",
"http://www.iqiyi.com/lib/m_208436914.html",
"http://www.iqiyi.com/lib/m_208432914.html",
"http://www.iqiyi.com/lib/m_208397814.html",
"http://www.iqiyi.com/lib/m_208324214.html",
"http://www.iqiyi.com/lib/m_208273814.html",
"http://www.iqiyi.com/lib/m_208273814.html",
"http://www.iqiyi.com/lib/m_208265414.html",
"http://www.iqiyi.com/lib/m_208259414.html",
"http://www.iqiyi.com/lib/m_208246114.html",
"http://www.iqiyi.com/lib/m_208205714.html",
"http://www.iqiyi.com/lib/m_208119714.html",
"http://www.iqiyi.com/lib/m_208073314.html",
"http://www.iqiyi.com/lib/m_208073314.html",
"http://www.iqiyi.com/lib/m_208073114.html",
"http://www.iqiyi.com/lib/m_208073114.html",
"http://www.iqiyi.com/lib/m_208072514.html",
"http://www.iqiyi.com/lib/m_208072014.html",
"http://www.iqiyi.com/lib/m_207974514.html",
"http://www.iqiyi.com/lib/m_207539014.html",
"http://www.iqiyi.com/lib/m_207496914.html",
"http://www.iqiyi.com/lib/m_207443814.html",
"http://www.iqiyi.com/lib/m_207267414.html",
"http://www.iqiyi.com/lib/m_207114614.html",
"http://www.iqiyi.com/lib/m_206518414.html",
"http://www.iqiyi.com/lib/m_206407614.html",
"http://www.iqiyi.com/lib/m_206401714.html",
"http://www.iqiyi.com/lib/m_206400214.html",
"http://www.iqiyi.com/lib/m_206275514.html",
"http://www.iqiyi.com/lib/m_206275414.html",
"http://www.iqiyi.com/lib/m_206275414.html",
"http://www.iqiyi.com/lib/m_206243214.html",
"http://www.iqiyi.com/lib/m_206035314.html",
"http://www.iqiyi.com/lib/m_205516314.html",
"http://www.iqiyi.com/lib/m_205513014.html",
"http://www.iqiyi.com/lib/m_205362214.html",
"http://www.iqiyi.com/lib/m_205362214.html",
"http://www.iqiyi.com/lib/m_205360714.html",
"http://www.iqiyi.com/lib/m_205360614.html",
"http://www.iqiyi.com/lib/m_205360614.html",
"http://www.iqiyi.com/lib/m_205353114.html",
"http://www.iqiyi.com/lib/m_205352814.html",
"http://www.iqiyi.com/lib/m_205349614.html",
"http://www.iqiyi.com/lib/m_205085114.html",
"http://www.iqiyi.com/lib/m_205077214.html",
"http://www.iqiyi.com/lib/m_205076914.html",
"http://www.iqiyi.com/lib/m_205076414.html",
"http://www.iqiyi.com/lib/m_201098714.html",
]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "iqiyi_movie_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = 1

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
        pcUrl = ""
        poster = ""
        point = 0.0
        alias = ""
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""
        playLength = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        mainId_r = re.search(r'lib/(.*?)\.html'.decode('utf8'),seed)
        if mainId_r:
            mainId = mainId_r.group(1)

        poster_p = soup.find("div", attrs={'class': 'result_pic'})
        if poster_p is not None:
            poster_p_tag = poster_p.find('img')
            if poster_p_tag is not None:
                poster = poster_p_tag.get('src')
            name_p = poster_p.find('a')
            if name_p is not None:
                name = name_p.get('title')
                pcUrl = name_p.get('href')

        point_P = soup.find('span',attrs={'class': 'score_font'})
        if point_P is not None:
            point_r = re.search(r'\d+.\d+'.decode('utf8'), point_P.get_text())
            if point_r:
                point = point_r.group()

        detail = soup.find("div", attrs={"class": "result_detail"})
        if detail is not None:
            for p_tag in detail.find_all("div", attrs={"class": "topic_item clearfix"}):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("看点：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search(r"别名： 暂无".decode("utf8"),p_tag.get_text()) is not True \
                    and re.search(r"别名：(.*?)".decode("utf8"),p_tag.get_text()):
                    alias = re.search(r"别名：(.*?)".decode("utf8"),p_tag.get_text()).group(1)
                if re.search(r"上映时间：[^\\]*?(\d\d\d\d)".decode("utf8"), p_tag.get_text()):
                    shootYear = re.search(r"上映时间：[^\\]*?(\d\d\d\d)".decode("utf8"),p_tag.get_text()).group(1)
                if re.search(r"片长：[^\\]*?(\d+)".decode("utf8"),p_tag.get_text()):
                    playLength = re.search(r"片长：[^\\]*?(\d+)".decode("utf8"),p_tag.get_text()).group(1)


        content_p = soup.find('p',  attrs={"data-movlbshowmore-ele":"whole"})
        if content_p is not None:
                intro = content_p.get_text().strip()


        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program['pcUrl'] = pcUrl
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program["point"] = float(point)
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        print name,pcUrl
        self.program_sub['playLength'] = playLength + ':' + '00'
        self.secondSpider()

    def secondSpider(self):
            self.program_sub['setNumber'] = 1
            self.program_sub['setName'] = self.program["name"]
            self.program_sub['webUrl'] = self.program['pcUrl']
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = iqiyi_movie_1()
    app.doProcess()