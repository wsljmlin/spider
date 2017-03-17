#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import urllib
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_yehetang_tv():
    def __init__(self):
        print "Do spider all_yehetang_tv."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://www.yehetang.com/pd/2-1.html"
                         , "http://www.yehetang.com/pd/2-1.html"
                         , "http://www.yehetang.com/pd/2-2.html"
                         , "http://www.yehetang.com/pd/2-3.html"
                         , "http://www.yehetang.com/pd/2-4.html"
                         , "http://www.yehetang.com/pd/2-5.html"
                         , "http://www.yehetang.com/pd/2-6.html"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.ctype = {}
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_yehetang_tv_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")

            seed_P = soup.find("div", attrs={"class": "k_list-1a"})
            if seed_P is not None:
                # print(seed_P)
                div_list = seed_P.find_all("div", attrs={"class": "k_list-lb"})
                for div in div_list:
                    # print(div)
                    a_tag = div.find("a")
                    if a_tag is not None:
                        subSeed = a_tag.get("href")
                        if subSeed is not None:
                            subSeed = "http://www.yehetang.com%s" % subSeed
                            self.seedList.append(subSeed)
                        ctype_p = div.find('div', attrs={'id': 'k_sou-4c-c'})
                        if ctype_p is not None:
                            ctype = ctype_p.find('a').get_text()
                            ctype = ','.join(ctype.split())
                            self.ctype[subSeed] = ctype
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '野荷塘'.decode("utf8")
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


        detail_p = soup.find("div", attrs={'class': 'k_jianjie'})
        if detail_p is not None:
            #get poster
            poster_p = detail_p.find("div", attrs={'id': 'k_jianjie-2b'})
            if poster_p is not None and poster_p.find('img') is not None:
                poster = poster_p.find('img').get('src')
                name = poster_p.find('img').get('alt')

            #get detail
            detail_1 = detail_p.find("div", attrs={'id': 'k_jianjie-3a'})
            if detail_1 is not None:
                detail_list = detail_1.find_all('ul')
                if detail_list is not None:
                    for ul in detail_list:
                        ul_p = str(ul)
                        if ul.find('li').get('class') == ['k_jianjie-3a-1-name'] and name == "":
                            name = ul.find('li').get_text()
                        elif re.search(r'状态：'.decode('utf8'), ul_p.decode('utf8')):
                            if re.search(r'预告'.decode('utf8'), ul_p.decode('utf8')):
                                return
                        elif re.search(r'别名：'.decode('utf8'), ul_p.decode('utf8')):
                           alias_p = ul.find_all('li')
                           alias = ""
                           for li in alias_p:
                                if not re.search(r'别名：'.decode('utf8'), (str(li)).decode('utf8')):
                                    alias = li.get_text()
                        elif re.search(r'导演：'.decode('utf8'), ul_p.decode('utf8')):
                            director_p = ul.find_all('li')
                            for li in director_p:
                                if not re.search(r'导演：'.decode('utf8'), (str(li)).decode('utf8')):
                                    director_p = li.get_text().strip()
                                    director_p = director_p.replace('/', '')
                                    director = ','.join(director_p.split())
                        elif re.search(r'演员：'.decode('utf8'), ul_p.decode('utf8')):
                            star_p = ul.find_all('li')
                            for li in star_p:
                                if not re.search(r'演员：'.decode('utf8'), (str(li)).decode('utf8')):
                                    star_p = li.get_text().strip()
                                    star_p = star_p.replace('/', '')
                                    star = ','.join(star_p.split())
                        elif re.search(r'地区：'.decode('utf8'), ul_p.decode('utf8')):
                            area_p = ul.find_all('li')
                            for li in area_p:
                                if not re.search(r'地区：'.decode('utf8'), (str(li)).decode('utf8')):
                                    area = li.get_text().strip()
                        elif re.search(r'语言：'.decode('utf8'), ul_p.decode('utf8')):
                            language_p = ul.find_all('li')
                            for li in language_p:
                                if not re.search(r'语言：'.decode('utf8'), (str(li)).decode('utf8')):
                                    programLanguage = li.get_text().strip()
                        elif re.search(r'剧情：'.decode('utf8'), ul_p.decode('utf8')):
                            intro_p = ul.find_all('li')
                            for li in intro_p:
                                if not re.search(r'剧情：'.decode('utf8'), (str(li)).decode('utf8')):
                                    intro = li.get_text().strip()
        #get mainId
        if re.match(r'http://www\.yehetang\.com/movie/(.*)\.html', seed):
            mainId = re.match(r'http://www\.yehetang\.com/movie/(.*)\.html', seed).group(1)

        if self.ctype.get(seed):
            ctype = self.ctype[seed]

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        video_p = soup.find('div', attrs={'id':'play_1'})
        if video_p is not None:
            video_list = video_p.find_all('li')
            self.secondSpider(video_list)

    def secondSpider(self, video_list):
        #for crask
        videoinfo_list = []
        crack_seed = "http://www.yehetang.com%s" % video_list[0].find('a').get('href')
        doc = spiderTool.getHtmlBody(crack_seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        videoinfo = ""
        videoinfo_p = soup.find_all("script")
        for info in videoinfo_p:
            if re.search(r'VideoInfoList=\"(.*)\"', str(info)):
                videoinfo_p = re.search(r'VideoInfoList=\"(.*)\"', str(info))
                if videoinfo_p is not None:
                    videoinfo = videoinfo_p.group(1)
                    videoinfo = str(videoinfo)
                    videoinfo_list = videoinfo.split('#')
                    # check
        if len(video_list) != len(videoinfo_list) or len(video_list) == 0 or len(videoinfo_list) == 0:
            return
        subprog_count = 0
        for video in video_list:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            webUrl = "http://www.yehetang.com%s" % video.find('a').get('href')
            setName = video.get_text()
            if re.search(r'(\d+)集'.decode('utf8'), setName):
                setNumber = re.search(r'(\d+)集'.decode('utf8'), setName).group(1)
            elif re.search(r'(\d+)'.decode('utf8'), setName):
                setNumber = re.search(r'(\d+)'.decode('utf8'), setName).group(1)

            subprog_count = subprog_count + 1
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == "" \
                    or setNumber is None or setName is None or webUrl is None:
                continue

            #check
            videoinfo_tmp = str(videoinfo_list[int(subprog_count-1)])
            if re.search(r'(\d+)集'.decode('utf-8'), videoinfo_tmp.decode('utf-8')):
                videoinfo_num = re.search(r'(\d+)集'.decode('utf-8'), videoinfo_tmp.decode('utf-8')).group(1)
                if videoinfo_num == setNumber:
                    parm = urllib.quote(videoinfo_tmp)
                    webUrl = "%s###%s" % (webUrl, parm)
            elif re.search(r'(\d+)'.decode('utf-8'), videoinfo_tmp.decode('utf-8')):
                videoinfo_num = re.search(r'(\d+)'.decode('utf-8'), videoinfo_tmp.decode('utf-8')).group(1)
                if videoinfo_num == setNumber:
                    parm = urllib.quote(videoinfo_tmp)
                    webUrl = "%s###%s" % (webUrl, parm)


            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_yehetang_tv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
