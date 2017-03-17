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
#重生之名流巨星


class qq_tv_1():
    def __init__(self):
        print "Do spider qq_tv_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://film.qq.com/cover/f/fdug0j3etx4ioja.html"]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "qq_tv_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])

            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        poster = ""
        star = ""
        director = ""
        ctype = ""
        shootYear = ""
        intro = ""
        mainId = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("span",attrs={'class': 'a_cover'})
        if poster_p is not None:
            poster = poster_p.find("img").get("lz_src")

        starts_P = soup.find("dd", attrs={"class": "actor"})
        if starts_P is not None:
            start_list = []
            for each in starts_P.find_all('a'):
                start_list.append(each.get_text())
            star = ",".join(start_list)

        detail = soup.find("dd", attrs={"class": "type"})
        for each in detail.find_all("span",  attrs={"class": "item"}):
            if re.search("导演：".decode("utf8"),each.get_text()):
                director = each.get_text().split("导演：".decode("utf8"))[1]
            if re.search("类型：".decode("utf8"),each.get_text()):
                ctype = each.get_text().split("类型：".decode("utf8"))[1]
            if re.search("年份：".decode("utf8"),each.get_text()):
                shootYear = each.get_text().split("年份：".decode("utf8"))[1]
            if re.search("地区：".decode("utf8"),each.get_text()):
                area = each.get_text().split("地区：".decode("utf8"))[1]

        content_p = soup.find('p',  attrs={"class": "detail_all"})
        if content_p is not None:
            if re.search("简介：".decode("utf8"),content_p.get_text()):
                intro = content_p.get_text().split("简介：".decode("utf8"))[1].strip()

        if re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed):
            mainId = re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed).group(2)
        name = soup.find("h3",attrs={'class':'film_name'}).get_text()
        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        seed_sub = 'http://s.video.qq.com/loadplaylist?vkey=897_qqvideo_cpl_%s_qq' % mainId
        self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("episode")
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""

            setNumber = each.get_text()
            setName = each.find_next_sibling("title").get_text()
            webUrl = each.find_next_sibling("url").get_text()
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = qq_tv_1()
    app.doProcess()