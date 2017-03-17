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


class ablum_youku_game():
    def __init__(self):
        print "Do spider ablum_youku_game."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://i.youku.com/i/UMjk2NTYwNTY0OA==/videos'#WCA世界电子竞技大赛
                        ,'http://i.youku.com/i/UMjk2NTYwNTY0OA==/videos'#WCA世界电子竞技大赛
                        ,'http://i.youku.com/u/UMTQ5OTEzNjU1Ng==/videos'#ImbaTV
                        ,'http://i.youku.com/u/UMzk3MjYyMjQ0/videos'#MarsTV
                        ,'http://i.youku.com/i/UMTczNjE5OTcwMA==/videos'#飞熊TV
                        ,'http://i.youku.com/i/UNTc5NjMxMjMy/videos'#游久微视频
                        ,'http://i.youku.com/i/UMTQ0NDQ1MDE3Mg==/videos'#CGA_TV
                        ,'http://i.youku.com/i/UMjc1MjAyMTM2/videos'#星际青年笨哥
                        ,'http://i.youku.com/i/UNTA0NjQ1OTcy/videos'#FallenAngel
                        ,'http://i.youku.com/i/UMTAxMTA2MDY0/videos'#游戏风云gamefy
                        ,'http://i.youku.com/i/UNjIwMzM0MDU2/videos'#GGwpTV
                        ,'http://i.youku.com/i/UNTg1MzY0OTY0/videos'#夜魔解说
                        ,'http://i.youku.com/i/UMzUxMTExMjM2/videos'#木有新闻
                        ,'http://i.youku.com/u/UMTc3MDAxMjU5Mg==/videos'#战旗全明星
                        ,'http://i.youku.com/i/UMzIwNjI4MTk2/videos'#TeamWE
                        ,'http://i.youku.com/i/UODkzNTkxMzY=/videos'#NeoTV
                        ,'http://i.youku.com/i/UMTI4NjUyMzg1Mg==/videos'#二龙
                        ,'http://i.youku.com/i/UMTgzMjQwODY4/videos'#小杰
                        ,'http://i.youku.com/i/UNDA5OTk3ODQ4/videos'#月爱
                        ,'http://i.youku.com/u/UMTI5MzUyNjEyMA==/videos'#七煌KeaHoarl
                        ,'http://i.youku.com/i/UMjE2NjAwODc2/videos'#天策
                        ,'http://i.youku.com/i/UMzE5NzMzNzM2/videos'#少帮主
                        ,'http://i.youku.com/i/UMzY0Njk2OTAw/videos'#D8TV
                        ,'http://i.youku.com/i/UNTU1Mzg3Mzk2/videos'#籽岷
                        ,'http://i.youku.com/i/UMzA2NjgyMDY5Mg==/videos'#小本解说
                        ,'http://i.youku.com/i/UMjQ5MTg4OTcy/videos'#夏一可
                        ,'http://i.youku.com/i/UMzE3MTA5NjQxNg==/videos'#守望先锋运营团队
                        ,'http://i.youku.com/i/UMzgwNDU2Mjg0/videos'#shy李晓峰
                        ,'http://i.youku.com/i/UMTQwOTY5MDQzNg==/videos'#笨熊
                        ,'http://i.youku.com/i/UNTQzNjM3MDIw/videos'#极光Oval
                        ,'http://i.youku.com/i/UMzA2Nzg1MDMxMg==/videos'#东三名流
                        ,'http://i.youku.com/i/UNTcwMDYzOTY4/videos'#妞宝宝
                        ,'http://i.youku.com/i/UMTQ4NzM5MTAyNA==/videos'#诺含
                        ,'http://i.youku.com/i/UMjk4NjY2NDQxMg==/videos'#阿姆西
                        ,'http://i.youku.com/i/UMTM4NDYxODc1Mg==/videos'#阳光
                        ,'http://i.youku.com/i/UMjkyMTUzNzc0MA==/videos'#瑞格
                        ,'http://i.youku.com/u/UMzc0NzQ2NDg0/videos'#lion大帝
                        ,'http://i.youku.com/i/UMzEyNjI2NjQ2OA==/videos'#马甲牧师
                        ,'http://i.youku.com/i/UNDM0MzQxMDI4/videos'#老白
                        ,'http://i.youku.com/i/UMzY3NDMzODIzNg==/videos'#咸鱼
                        ,'http://i.youku.com/u/UMTM4ODg1NjE3Mg==/videos'#炉石传说运营团队

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_youku_game_" + self.today + ".txt")
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
            #print self.program['name'], self.program['totalSets']
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
        ctype = ""
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
    app = ablum_youku_game()
    app.doProcess()