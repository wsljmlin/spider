#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderTool import spiderTool
from vipmediaContent import BASE_CONTENT
from vipmediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class all_iqiyi_vipmovie():
    def __init__(self):
        print "Do spider all_iqiyi_vipmovie."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.iqiyi.com/www/1/----------2---4-1-1-iqiyi--.html"
                         , "http://list.iqiyi.com/www/1/----------2---4-1-1-iqiyi--.html"
                         , "http://list.iqiyi.com/www/1/----------2---4-2-1-iqiyi--.html"
                         , "http://list.iqiyi.com/www/1/----------2---4-3-1-iqiyi--.html"
                         , "http://list.iqiyi.com/www/1/----------2---4-4-1-iqiyi--.html"
                         , "http://list.iqiyi.com/www/1/----------2---4-5-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-6-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-7-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-8-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-9-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-10-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-11-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-12-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-13-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-14-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-15-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-16-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-17-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-18-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-19-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-20-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-21-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-22-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-23-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-24-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-25-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-26-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-27-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-28-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-29-1-iqiyi--.html"
                         # , "http://list.iqiyi.com/www/1/----------2---4-30-1-iqiyi--.html"
                        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.seqNocnt = 1
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_iqiyi_vipmovie_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("div", attrs={"class": "wrapper-piclist"})
            if seed_P is not None:
                seedList = seed_P.find_all("div", attrs={"class": "site-piclist_pic"})
            for each in seedList:
                #pass the vip quan
                vip_ticket = each.find('span', attrs={'class': 'icon-vip-quan'})
                if vip_ticket is not None:
                    continue
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        if re.match(r'http://www\.iqiyi\.com/v_\w+\.html', subSeed) or re.match(r'http://www\.iqiyi\.com/dianying/\d{8}/', subSeed):
                            self.seedList.append(subSeed)
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.firstSpider(seed)
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            # print self.program['name'], self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            if re.search(r'预告'.decode('utf8'), self.program['name']) or self.program_sub['setNumber']  == "" \
                or self.program_sub['setName'] == "" or self.program_sub['webUrl'] == ""\
                or self.program_sub['setNumber']  is None \
                or self.program_sub['setName'] is None or self.program_sub['webUrl'] is None:
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
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""
        shootYear = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        tvId = re.search(r'data-player-tvid="([^"]+?)"', doc)
        videoId = re.search(r'data-player-videoid="([^"]+?)"', doc)
        if tvId and videoId:
            newUrl = 'http://cache.video.qiyi.com/vi/%s/%s/' % (tvId.group(1), videoId.group(1))
            doc = spiderTool.getHtmlBody(newUrl)
        else:
            return

        try:
            json_data = json.loads(doc)
            name = json_data["shortTitle"]
            poster = json_data["apic"]
            star = json_data["ma"].replace("|", ",")
            director = json_data["d"].replace("|", ",")
            ctype = json_data["tg"].replace(" ", ",")
            area = json_data["ar"]
            intro = json_data["info"]
        except:
            return

        #speical deal
        if re.search(r'华语'.decode('utf-8'), ''.join(area)):
            area = u'中国'



        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        if re.match(r'http://www\.iqiyi\.com/v_(\w+)\.html', seed):
            mainId = re.match(r'http://www\.iqiyi\.com/v_(\w+)\.html', seed).group(1)
        elif re.match(r'http://www\.iqiyi\.com/dianying/(\d{8})/', seed):
            mainId = re.match(r'http://www\.iqiyi\.com/dianying/(\d{8})/', seed).group(1)
        self.program["mainId"] = mainId

        self.secondSpider()

    def secondSpider(self):
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.program_sub['setNumber'] = 1
        self.program_sub['setName'] = self.program['name']
        self.program_sub['webUrl'] = self.program['pcUrl']
        if len(self.program['poster']) > 0:
            self.program_sub['poster'] = self.program['poster'][0]['url']
        self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_iqiyi_vipmovie()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
