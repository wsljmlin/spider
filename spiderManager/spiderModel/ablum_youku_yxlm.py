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


class ablum_youku_yxlm():
    def __init__(self):
        print "Do spider ablum_youku_yxlm."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://i.youku.com/i/UMzc2NTY2MjM2/videos'#董小飒
                        ,'http://i.youku.com/i/UMzc2NTY2MjM2/videos'#董小飒
                        ,'http://i.youku.com/u/UMTc2NTAwNTk4OA==/videos'#文森特
                        ,'http://i.youku.com/u/UMTA1NTY0Njg=/videos'#徐老师
                        ,'http://i.youku.com/i/UMTc2MTgyNDk2/videos'#秀依
                        ,'http://i.youku.com/i/UMTU0NjE3NDk2/videos'#WoDotA
                        ,'http://i.youku.com/u/UMzk2ODA1OTY4/videos'#Miss排位日记
                        ,'http://i.youku.com/i/UMjYwMzE0NzMy/videos'#起小点
                        ,'http://i.youku.com/i/UMTQxMzk3NTE4NA==/videos'#SilenceOB
                        ,'http://i.youku.com/i/UMTkyOTQ1MzAw/videos'#兔玩网
                        ,'http://i.youku.com/i/UMTM3OTEyODgxMg==/videos'#超神解说
                        ,'http://i.youku.com/i/UMTQ2MjAzMzgxMg==/videos'#聚印象
                        ,'http://i.youku.com/u/UMzY1NTQ1NTc2/videos'#小苍
                        ,'http://i.youku.com/i/UMzUwMzI3NjQw/videos'#三眼解说
                        ,'http://i.youku.com/i/UNDQ2Mjc0NTI4/videos'#Yuki酱丶
                        ,'http://i.youku.com/i/UMTYxNTkyNzIyOA==/videos'#小学生院长
                        ,'http://i.youku.com/i/UMjgzNjU1MTQ4MA==/videos'#RIOT拳头游戏
                        ,'http://i.youku.com/i/UMTQzNDAxMDA1Ng==/videos'#Xz无名
                        ,'http://i.youku.com/u/UNTY5ODgwMzY=/videos'#伪伪酱
                        ,'http://i.youku.com/u/UNTUyNDMyODQ0/videos'#伊芙蕾雅
                        ,'http://i.youku.com/i/UNjk1MTczNg==/videos'#小东
                        ,'http://i.youku.com/i/UNjI2NTcxODI0/videos'#纱布德
                        ,'http://i.youku.com/u/UMTM2MjU5MDg2OA==/videos'#Numen精彩集锦
                        ,'http://i.youku.com/i/UMTMwMjY3NTU4NA==/videos'#大司马
                        ,'http://i.youku.com/i/UMTk0NDY0ODA5Mg==/videos'#小数点大人
                        ,'http://i.youku.com/u/UMjI5NTE5NDcy/videos'#安静苦笑
                        ,'http://i.youku.com/u/UNTE0MjQyODM2/videos'#教主
                        ,'http://i.youku.com/i/UMTgyMTQ0MjY0MA==/videos'#江湖人称一条柴
                        ,'http://i.youku.com/i/UMzYzMzA4NDA0/videos'#枪炮玫瑰
                        ,'http://i.youku.com/i/UMzIxNTY1NzQ2OA==/videos'#NiceTV
                        ,'http://i.youku.com/i/UMTM4NzE5NzkwOA==/videos'#倒影
                        ,'http://i.youku.com/i/UNTkwODc1NDA=/videos'#峰峰侠
                        ,'http://i.youku.com/u/UNzg2MTczNzI=/videos'#拳师七号
                        ,'http://i.youku.com/i/UNDU3NzQ3Mg==/videos'#西瓜教学
                        ,'http://i.youku.com/u/UMzA2MDg3Njc2/videos'#JY解说
                        ,'http://i.youku.com/i/UMzkyMjkzNTQ4/videos'#虫仔
                        ,'http://i.youku.com/u/UMzQ3MTUxNTAw/videos'#Misaya若风
                        ,'http://i.youku.com/i/UMTg0MzIyMjMyNA==/videos'#撸啊撸yk
                        ,'http://i.youku.com/i/UMjgzMjA4Njk2/videos'#信一
                        ,'http://i.youku.com/i/UNDIzMDE5NDM2/videos'#WinGinglol
                        ,'http://i.youku.com/i/UNTY0NDEyMDE2/videos'#宇宙解说
                        ,'http://i.youku.com/i/UNDQ2NTU1MDA=/videos'#YD
                        ,'http://i.youku.com/i/UMTM3NDI4MDg0/videos'#Funlol
                        ,'http://i.youku.com/i/UMzkxMDU2NDY0/videos'#Lin小北
                        ,'http://i.youku.com/u/UNDQxMTk2MjQ4/videos'#诅咒
                        ,'http://i.youku.com/i/UNDE5MjgwMTc2/videos'#冬阳
                        ,'http://i.youku.com/i/UMzQ1NDU3MjA4/videos'#解说小漠
                        ,'http://i.youku.com/i/UMjUyNDU5ODY4/videos'#小树解说
                        ,'http://i.youku.com/i/UNDUzMTUzMjA4/videos'#GN视界
                        ,'http://i.youku.com/i/UMTQ4NzMyMjA0OA==/videos'#布姆
                        ,'http://i.youku.com/i/UMjk3MDc4MDY4/videos'#辛巴达


        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_youku_yxlm_" + self.today + ".txt")
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
        ctype = "英雄联盟".decode('utf8')
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
    app = ablum_youku_yxlm()
    app.doProcess()