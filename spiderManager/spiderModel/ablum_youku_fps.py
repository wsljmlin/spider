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
#木下大胃王


class ablum_youku_fps():
    def __init__(self):
        print "Do spider ablum_youku_fps."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://i.youku.com/i/UMTIwMjA3MzkwNA==/videos'#空明
                        ,'http://i.youku.com/i/UMTIwMjA3MzkwNA==/videos'#空明
                        ,'http://i.youku.com/i/UNDI1NDgwNTcy/videos'#亡灵
                        ,'http://i.youku.com/i/UMTkwMjA1ODAw/videos'#杀舞赦
                        ,'http://i.youku.com/i/UMzgyNzcyMDI4/videos'#老李船长
                        ,'http://i.youku.com/u/UNTYyOTA3NDQ0/videos'#alex
                        ,'http://i.youku.com/i/UMzY1MjI5NjYw/videos'#气宇菲凡
                        ,'http://i.youku.com/u/UMzg0NTYwMjg4/videos'#初恋
                        ,'http://i.youku.com/i/UMjUyMjI3OTE2/videos'#豪宝宝
                        ,'http://i.youku.com/u/UMzQxMzQ1NjU0MA==/videos'#陈子豪
                        ,'http://i.youku.com/i/UMzM2OTM2NDQ4/videos'#CH明明

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_youku_fps_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "游戏".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            #print self.program['name'], self.program['totalSets'], self.program['mainId']
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
        star = ""
        ctype = "FPS"
        shootYear = ""
        intro = ""
        mainId = ""
        area = ""
        point = 0.0
        playTimes = 0

        mainId_p = re.search(r'http://i.youku.com/i/(.+)/videos', seed)
        if mainId_p:
            mainId = mainId_p.group(1)
        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("div",attrs={'class':'head-avatar'})
        poster_p1 = soup.find("div",attrs={'class':'avatar'})
        if poster_p is not None:
            poster_a = poster_p.find('a')
            if poster_a is not None:
                name = poster_a.get("title")
            if poster_p.find('img') is not None:
                poster = poster_p.find("img").get("src")
        elif poster_p1 is not None:
            if poster_p1.find('img') is not None:
                poster = poster_p1.find("img").get("src")
                name = poster_p1.find("img").get("title")

        content_p = soup.find('div',  attrs={"class": "userintro"})
        if content_p is not None:
            content = content_p.find('div', attrs={'class': 'desc'})
            if content is not None:
                intro = content.get_text().strip().split('自频道介绍：'.decode('utf8'))[1]

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        self.program['point'] = point
        self.program['playTimes'] = playTimes

        pages = 0
        total_num_p = soup.find_all('div', attrs={'class': 'title'})
        for item in total_num_p:
            if re.search(r'视频[^\\]*?\((\d+)\)'.decode('utf8'), item.get_text().replace(',','')):
                total_num = re.search(r'\((\d+)\)', item.get_text().replace(',','')).group(1)
                pages = int(total_num)/40 + 2
        if pages ==0:
            total_num_p = soup.find('span', attrs={'class': 'append'})
            if total_num_p is not None and re.search(r'共(\d+)个视频'.decode('utf8'), total_num_p.get_text().replace(',','')):
                total_num = re.search(r'共(\d+)个视频'.decode('utf8'), total_num_p.get_text().replace(',','')).group(1)
                pages = int(total_num)/40 + 2
        if pages > 20:
            pages = 20
        if pages != 0:
            for page in range(1, pages):
                sub_seed = seed + '/fun_ajaxload/?page_num=%d&page_order=0' %(page)
                self.secondSpider(sub_seed)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_pog = sub_soup.find_all("div", attrs={'class': 'v va'})
        if len(sub_pog) == 0:
            sub_pog = sub_soup.find_all("div", attrs={'class': 'yk-col4'})
        for each in sub_pog:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            poster = ''
            setName = ""
            webUrl = ""
            playLength = ''

            setNumber_p = each.find('span', attrs={'class': 'v-upload-date'})
            if setNumber_p is not None:
                if re.search(r'\d+-\d+-\d+'.decode('utf8'), setNumber_p.get_text()):
                    setNumber = re.search(r'\d+-\d+-\d+'.decode('utf8'),  setNumber_p.get_text()).group().replace('-'.decode('utf8'),'')
                elif re.search(r'\d+-\d+'.decode('utf8'), setNumber_p.get_text()):
                    year = time.strftime('%Y',time.localtime(time.time()))
                    setNumber = year + re.search(r'\d+-\d+'.decode('utf8'), each.get_text()).group().replace('-'.decode('utf8'),'')

            if re.search(r'\d+-\d+-\d+'.decode('utf8'), each.get_text()):
                setNumber = re.search(r'\d+-\d+-\d+'.decode('utf8'),  each.get_text()).group().replace('-'.decode('utf8'),'')
            elif re.search(r'\d+-\d+'.decode('utf8'), each.get_text()):
                year = time.strftime('%Y',time.localtime(time.time()))
                setNumber = year + re.search(r'\d+-\d+'.decode('utf8'), each.get_text()).group().replace('-'.decode('utf8'),'')

            poster_p = each.find('img')
            if poster_p is not None:
                poster = poster_p.get('src')

            setName_p = each.find('div', attrs={'class': 'v-link'})
            if setName_p is not None:
                setName = setName_p.find('a').get('title')
                webUrl = setName_p.find('a').get('href')

            playLength_p = each.find('span', attrs={'class': 'v-time'})
            if playLength_p is not None:
                playLength = playLength_p.get_text()

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = ablum_youku_fps()
    app.doProcess()