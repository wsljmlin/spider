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



class ablum_youku_cartoon_1():
    def __init__(self):
        print "Do spider ablum_youku_cartoon_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = []
        self.seedList = ["http://www.youku.com/show_page/id_z31c53954e34c11e5a2a2.html" #双星之阴阳师
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_youku_cartoon_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program["name"],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        point = 0.0
        poster = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        mainId = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        seed_Re = re.search(r'http://www\.youku\.com/show_page/id', seed)
        if not seed_Re:
            seed_P = soup.find('h1', attrs={'class': 'title'})
            if seed_P is not None:
                seed_aTag = seed_P.find('a')
                if seed_aTag is not None:
                    seed = seed_aTag.get('href')
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc, from_encoding="utf8")

        point_P = soup.find('span',attrs={'class': 'rating'})
        if point_P is not None:
            if point_P.find('em',attrs={'class': 'num'}) is not None:
                point = point_P.find('em',attrs={'class': 'num'}).get_text()

        poster_p = soup.find("li",attrs={'class':'thumb'})
        if poster_p is not None:
            poster = poster_p.find('img').get("src")

        name_P = soup.find('h1', attrs={'class': 'title'})
        if name_P is not None:
            name_span = name_P.find('span', attrs={'class': 'name'})
            if name_span is not None:
                name = name_span.get_text()
            shootYear_P = name_P.find('span', attrs={'class': 'pub'})
            if shootYear_P is not None:
                shootYear_text = shootYear_P.get_text()
                if re.search(r'\d+', shootYear_text):
                    shootYear = re.search(r'\d+', shootYear_text).groups()

        alias_P = soup.find('span',attrs={'class': 'alias'})
        if alias_P is not None:
            alias = alias_P.get('title')

        area_P = soup.find('span',attrs={'class': 'area'})
        if area_P is not None:
            area_list = []
            for each in area_P.find_all("a"):
                area_list.append(each.get_text())
            area = ",".join(area_list)

        ctype_all = soup.find_all("span", attrs={"class": "type"})
        for ctype_P in ctype_all:
            if re.search(r'类型:'.decode('utf8'), ctype_P.get_text()):
                ctype_list = []
                for each in ctype_P.find_all('a'):
                    ctype_list.append(each.get_text())
                ctype = ",".join(ctype_list)

        star_P = soup.find("span", attrs={"class": "actor"})
        if star_P is not None:
            star_list = []
            for each in star_P.find_all('a'):
                star_list.append(each.get_text())
            star = ",".join(star_list)

        director_P = soup.find("span", attrs={"class": "director"})
        if director_P is not None:
            director_list = []
            for each in director_P.find_all('a'):
                director_list.append(each.get_text())
            director = ",".join(director_list)

        playTimes_P = soup.find('span', attrs={'class': 'play'})
        if playTimes_P is not None:
            playTimesStr = playTimes_P.get_text()
            playTimes_list = re.findall(r'(\d+)', playTimesStr)
            playTimes = long(''.join(playTimes_list))

        content_p = soup.find('span',  attrs={"class": "short", 'id': 'show_info_short'})
        if content_p is not None:
                intro = content_p.get_text().strip()

        if re.match(r'http://www\.youku\.com/show_page/(id_(\w+))\.html', seed):
            mainId = re.match(r'http://www\.youku\.com/show_page/(id_(\w+))\.html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        urlList = re.findall(r'<li\s+data="(reload_\d+)"\s*(class="current"){0,1}\s*>', doc)
        if urlList:
                for url in urlList:
                    seed_sub = 'http://www.youku.com/show_point/%s.html?dt=json&divid=point_%s&tab=0&__rt=1&__ro=point_%s' % (mainId, url[0], url[0])
                    self.secondSpider(seed_sub)
        else:
                seed_sub = 'http://www.youku.com/show_point/%s.html?dt=json&divid=point_reload_1&tab=0&__rt=1&__ro=point_reload_1' % mainId
                self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("div", attrs={'class': 'item'})
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            playLength = ""
            setIntro = ""
            plot = []

            setName_P = each.find('div', attrs={'class': 'link'})
            if setName_P is not None:
                setName = setName_P.find('a').get('title').strip()
                webUrl = setName_P.find('a').get('href')
                if re.search(r'\d+$'.decode('utf8'), setName):
                    setNumber = re.search(r'\d+$'.decode('utf8'), setName).group()
                elif re.search(r'^\d+'.decode('utf8'), setName):
                    setNumber = re.search(r'^\d+'.decode('utf8'), setName).group()
                elif re.search(r'(\d+)话'.decode('utf8'), setName):
                    setNumber = re.search(r'(\d+)话'.decode('utf8'), setName).group(1)
                elif re.search(r'第(\d+)'.decode('utf8'), setName):
                    setNumber = re.search(r'第(\d+)'.decode('utf8'), setName).group(1)
                else:
                    setNumber = '1'

            poster_P = each.find('div', attrs={'class': 'thumb'})
            if poster_P is not None:
                poster = poster_P.find('img').get('src')

            playLength_P = each.find('div', attrs={'class': 'time'})
            if playLength_P is not None:
                playLength = playLength_P.get_text()

            setIntro_P = each.find('div', attrs={'class': 'desc'})
            if setIntro_P is not None:
                setIntro = setIntro_P.get_text()

            plot_P = each.find('div', attrs={'class': 'keylist'})
            if plot_P is not None:
                for item in plot_P.find_all('li'):
                    plot_dict = {}
                    plot_dict["time"] = item.find('em').get_text()
                    plot_dict["title"] = item.find('a').get_text()
                    plot.append(plot_dict)
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program_sub['plot'] = plot
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = ablum_youku_cartoon_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
    app.doProcess()