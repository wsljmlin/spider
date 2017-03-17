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
from vipmediaContent import BASE_CONTENT
from vipmediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_mgtv_vipmovie():
    def __init__(self):
        print "Do spider all_mgtv_vipmovie."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=1&pc=60"
                         , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=1&pc=60"
                         , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=2&pc=60"
                         , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=3&pc=60"
                         , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=4&pc=60"
                         , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=5&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=6&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=7&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=8&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=9&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=10&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=11&pc=60"
                         # , "http://s5.hunantv.com/v5/list/pc?ic=1&ty=3&chargeInfo=b2&if=0&sort=2&pn=12&pc=60"

        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.seqNocnt = 1
        self.prgdata = {}
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_mgtv_vipmovie_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            doc = spiderTool.getHtmlBody(seed)
            try:
                data = json.loads(doc)
            except:
                # print("load json error1111!")
                return
            if data.get('data') is None:
                # print("get html error1111")
                return
            elif data['data'].get('hitDocs') is None:
                return

            playId = ""
            clipId = ""
            soupdata = data['data']['hitDocs']
            for each in soupdata:
                if each.get('playPartId'):
                    playId = each['playPartId']
                if each.get('clipId'):
                    clipId = each['clipId']
                if clipId != "" and playId != "":
                    subseed = "http://www.mgtv.com/b/%s/%s.html" % (clipId, playId)
                    self.seedList.append(subseed)
                    if each.get('s_imgVerticalMpp'):
                        prgdata = {}
                        prgdata['poster'] = each['s_imgVerticalMpp']
                        self.prgdata[subseed] = prgdata

            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = '芒果TV'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            # add poster
            if self.prgdata.get(seed):
                poster = self.prgdata[seed]['poster']
                self.program['poster'] = spiderTool.listStringToJson('url', poster)
            #print self.program['name'], self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == '' or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            # add seqnum
            self.program['seqNo'] = self.seqNocnt
            self.seqNocnt = self.seqNocnt + 1

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

        mainId_p = re.findall(r'http://www\.mgtv\.com/\w/\d+/(.*)\.html', seed)
        if mainId_p:
            mainId = mainId_p[0]

        # get
        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        videoinfo = soup.find('div', attrs={'class': 'v-panel-info v-panel-mod'})
        if videoinfo is not None:
            pinfo_list = videoinfo.find_all('p')
            for pinfo in pinfo_list:
                pinfo_str = str(pinfo)
                # print(pinfo_str)
                if re.search(r'导演：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    director = pinfo.find('a').get_text()
                    if re.search(r'暂无'.decode('utf-8'), director) or re.search(r'未知'.decode('utf-8'), director):
                        director = ""
                elif re.search(r'主演：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    star_p = pinfo.find_all('a')
                    star_list = []
                    for li in star_p:
                        if not re.search(r'暂无'.decode('utf-8'), li.get_text()) or re.search(r'未知'.decode('utf-8'),
                                                                                            li.get_text()):
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
                        li.append(li.get_text())
                    ctype = ','.join(ctype_list)
                elif re.search(r'简介：'.decode('utf-8'), pinfo_str.decode('utf8')):
                    intro_p = pinfo.find('span', attr={'class': 'details'})
                    if intro_p is not None:
                        intro = intro_p.get_text()

        seedJson = ""
        if mainId != '':
            seedJson = "http://pcweb.api.mgtv.com/episode/list?video_id=%s&page=0&size=40" % mainId
        else:
            return

        json_data = ""
        # tatal_pages = 1
        # current_page = 0
        doc = spiderTool.getHtmlBody(seedJson)
        try:
            data = json.loads(doc)
        except:
            # print("load json error1111!")
            return
        if data.get('data') is None:
            # print("get html error1111")
            return

        json_data = data['data']
        # if json_data.get('total_page'):
        #     tatal_pages = json_data['total_page']
        if json_data.get('info'):
            name = json_data['info']['title']
            if intro == "":
                intro = json_data['info']['desc']
                # if json_data.get('current_page'):
                #     current_page = json_data['current_page']

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


        subseed = "http://pcweb.api.mgtv.com/movie/list?video_id=%s" % mainId
        self.secondSpider(subseed)



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
        if json_data.get('info'):
            info = json_data['info']
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''
            playLength = ""
            setIntro = ""

            if info.get('img'):
                poster = info['img']
            if info.get('url'):
                webUrl = "http://www.mgtv.com%s" % info['url']
            if info.get('title'):
                setName = info['title']
            if info.get('duration'):
                playLength_p = re.findall(r'\d+'.decode('utf-8'), info['duration'])
                playLength_d = int(playLength_p[0])
                playLength = self.minute2hms(playLength_d)
            setNumber = 1

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == "" \
                    or setNumber is None or setName is None or webUrl is None:
                return
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

    def minute2hms(self, min):
        hour = 0
        minute = 0

        if min <= 0:
            return
        if min//60 > 0:
            hour = min//60
            minute = min%60
            return "%02d:%02d:00" % (hour,minute)
        else:
            minute = min
            return "%02d:00" % (minute)



if __name__ == '__main__':
    app = all_mgtv_vipmovie()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
