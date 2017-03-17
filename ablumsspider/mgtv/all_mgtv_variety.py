#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import types
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
from collections import OrderedDict


class all_mgtv_variety():
    def __init__(self):
        print "Do spider all_mgtv_variety."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.mgtv.com/1/---------2-1-0--.html"
                         , "http://list.mgtv.com/1/---------2-1-0--.html"
                         , "http://list.mgtv.com/1/---------2-2-0--.html"
                         , "http://list.mgtv.com/1/---------2-3-0--.html"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.prgdata = {}
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_mgtv_variety_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            seedList = []
            self.seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("div", attrs={"class": "m-vlist v-list-v5 v-list"})
            if seed_P is not None:
                seedList = seed_P.find_all("li", attrs={"class": "v-item-v5 v-item-x $0"})
            for each in seedList:
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        self.seedList.append(subSeed)
                        if each.find('img') is not None:
                            prgdata = {}
                            prgdata['poster'] = each.find('img').get('src')
                            self.prgdata[subSeed] = prgdata
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = '芒果TV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            # add poster
            if self.prgdata.get(seed):
                poster = self.prgdata[seed]['poster']
                self.program['poster'] = spiderTool.listStringToJson('url', poster)
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            #reverse
            self.program['programSub'].reverse()

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')


    def firstSpider(self, seed):
        name = ""
        poster = ""
        point = 0.0
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""
        videoId=""

        mainId_p = re.findall(r'http://www\.mgtv\.com/\w/(.*)/.*\.html', seed)
        if mainId_p:
            mainId = mainId_p[0]
        videoId_p = re.findall(r'http://www\.mgtv\.com/\w/\d+/(.*)\.html', seed)
        if videoId_p:
            videoId = videoId_p[0]

        #get
        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        videoinfo = soup.find('div', attrs={'class': 'v-panel-info v-panel-mod'})
        if videoinfo is not None:
            pinfo_list = videoinfo.find_all('p')
            for pinfo in pinfo_list:
                pinfo_str = str(pinfo)
                if re.search(r'导演：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    director = pinfo.find('a').get_text()
                    if re.search(r'暂无'.decode('utf-8'), director) or re.search(r'未知'.decode('utf-8'), director):
                        director = ""
                elif re.search(r'主持：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    star_p = pinfo.find_all('a')
                    star_list = []
                    for li in star_p:
                        if not re.search(r'暂无'.decode('utf-8'), li.get_text()) or re.search(r'未知'.decode('utf-8'), li.get_text()):
                            star_list.append(li.get_text())
                    star = ','.join(star_list)
                elif re.search(r'地区：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    area_p = pinfo.find_all('a')
                    area_list = []
                    for li in area_p:
                        area_list.append(li.get_text())
                    area = ','.join(area_list)
                elif re.search(r'类型：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    ctype_p = pinfo.find_all('a')
                    ctype_list = []
                    for li in ctype_p:
                        ctype_list.append(li.get_text())
                    ctype = ','.join(ctype_list)
                elif re.search(r'简介：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    intro_p = pinfo.find('span',attrs={'class': 'details'})
                    if intro_p is not None:
                        intro = intro_p.get_text()

        seedJson = ""
        if mainId != '':
            seedJson = "http://pcweb.api.mgtv.com/variety/showlist?video_id=%s" % videoId
        else:
            return

        json_data = ""
        tatal_pages = 1
        current_page = 0
        doc = spiderTool.getHtmlBody(seedJson)
        try:
            data = json.loads(doc, object_pairs_hook=OrderedDict)
        except:
            # print("load json error1111!")
            return
        if data.get('data') is None:
            # print("get html error1111")
            return

        json_data = data['data']
        #get title
        if json_data.get('info'):
            name = json_data['info']['title']

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url', poster)
        self.program['point'] = point
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name', star)
        self.program['director'] = spiderTool.listStringToJson('name', director)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId


        #only get current data
        #cur cid
        curretId = ""
        if json_data.get('cur'):
            if json_data['cur'].get('cid'):
                curretId = json_data['cur']['cid']
        if json_data.get('tab_m') and curretId != "":
            for meach in json_data['tab_m']:
                subprgseed = "http://pcweb.api.mgtv.com/variety/showlist?collection_id=%s&month=%s" % (curretId, meach['m'])
                self.secondSpider(subprgseed)

        #get subseed, for all the data
        # if json_data.get('tab_y'):
        #     for yeach in json_data['tab_y']:
        #         subseed = "http://pcweb.api.mgtv.com/variety/showlist?collection_id=%s" % yeach['id']
        #         subdoc = spiderTool.getHtmlBody(subseed)
        #         try:
        #             subdata = json.loads(subdoc, object_pairs_hook=OrderedDict)
        #         except:
        #             # print("load json error1111!")
        #             return
        #         if subdata.get('data') is None:
        #             # print("get html error1111")
        #             return
        #         subjson_data = subdata['data']
        #         if subjson_data.get('tab_m'):
        #             for meach in subjson_data['tab_m']:
        #                 subprgseed = "http://pcweb.api.mgtv.com/variety/showlist?collection_id=%s&month=%s" % (yeach['id'], meach['m'])
        #                 self.secondSpider(subprgseed)
        #         else:
        #             continue
        #
        # else:
        #     return



    def secondSpider(self, subseed):
        doc = spiderTool.getHtmlBody(subseed)
        try:
            data = json.loads(doc)
        except:
            # print("load json error1111!")
            return
        if data.get('data') is None:
            # print("get html error1111")
            return

        json_data = data['data']
        if json_data.get('list'):
            for video in json_data['list']:
                self.program_sub = copy.deepcopy(PROGRAM_SUB)
                setNumber = ""
                setName = ""
                webUrl = ""
                poster = ''
                playLength = ""
                setIntro = ""

                if video.get('img'):
                    poster = video['img']
                if video.get('url'):
                    webUrl = "http://www.mgtv.com%s" % video['url']
                if video.get('t1'):
                    setName = video['t1']
                if video.get('t2'):
                    setNumber_p = video['t2']
                    if re.search(r':', setNumber_p):
                        playLength = setNumber_p
                        setNumber = "1"
                    else:
                        setNumber_p = setNumber_p.replace('-', '')
                        setNumber_p = re.findall(r'(\d+)', setNumber_p)
                        if setNumber_p:
                            setNumber = setNumber_p[0]

                if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                        or setNumber is None or setName is None or webUrl is None:
                    continue
                self.program_sub['setNumber'] = setNumber.replace('-', '')
                self.program_sub['setName'] = setName
                self.program_sub['webUrl'] = webUrl
                self.program_sub['poster'] = poster
                self.program_sub['playLength'] = playLength
                self.program_sub['setIntro'] = setIntro
                self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_mgtv_variety()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()