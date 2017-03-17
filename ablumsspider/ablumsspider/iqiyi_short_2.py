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


class iqiyi_short_2():
    def __init__(self):
        print "Do spider iqiyi_short_2."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.seedList = ["http://www.iqiyi.com/a_19rrgued6t.html"#1笑霸来了
                         ,"http://www.iqiyi.com/a_19rrgued6t.html"#1笑霸来了
                         ,"http://www.iqiyi.com/a_19rrgja8b5.html"#5、欢乐囧图 爱奇艺
                         ,'http://www.iqiyi.com/a_19rrgi8vad.html#vfrm=2-3-0-1'#戏说电影

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "iqiyi_short_2_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'], self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
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

        name_p = soup.find('a', attrs={'class': 'white'})
        if name_p is not None:
            name = name_p.get_text()

        poster_p = soup.find("ul", attrs={'class': 'album-imgs'})
        if poster_p is not None:
            if poster_p.find('img') is not None:
                poster = poster_p.find('img').get("src")


        starts_P = soup.find("dd", attrs={"class": "actor"})
        if starts_P is not None:
            start_list = []
            for each in starts_P.find_all('a'):
                start_list.append(each.get_text())
            star = ",".join(start_list)

        detail = soup.find("div", attrs={"class": "msg-hd-lt fl"})
        if detail is not None:
            for p_tag in detail.find_all('p'):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("配音：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str


        content_p = soup.find('div ',  attrs={"data-moreorless":"lessinfo"})
        if content_p is not None:
            if re.search("简介：".decode("utf8"),content_p.get_text()):
                intro = content_p.get_text().split("简介：".decode("utf8"))[1].strip()


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro

        seed_P = re.search(r'sourceId:\s*(?P<sourceId>\d+),\s*cid:\s*(?P<cid>\d+)', doc)
        if seed_P:
            sourceId = seed_P.group('sourceId')
            cid = seed_P.group('cid')
            self.program['mainId'] = sourceId
            if sourceId != '0':
                seed_sub = 'http://cache.video.iqiyi.com/jp/sdvlst/%s/%s/' %(cid,sourceId)
                self.secondSpider(seed_sub)
                return

        seed_P =  re.search(r'albumId:\s*(?P<albumId>\d+),[^\\]*?cid:\s*(?P<cid>\d+)', doc)
        if seed_P:
            albumId = seed_P.group('albumId')
            cid = seed_P.group('cid')
            self.program['mainId'] = albumId
            seed_sub = 'http://cache.video.qiyi.com/jp/avlist/%s/' %(albumId)
            self.secondSpider(seed_sub)
            return

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc.split('=', 1)[1])
        data = json_data["data"]
        if 'vlist' in data:
            data = data['vlist']
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ''
            setName = ''
            webUrl = ''
            poster = ''
            playLength = ''
            setIntro = ''
            if 'tvYear' in each:
                setNumber = each['tvYear']
            elif 'pds' in each:
                setNumber = each['pds']
            if 'videoName' in each:
                setName = each['videoName']
            elif 'shortTitle' in each:
                setName = each['shortTitle']
            if 'vUrl' in each:
                webUrl = each['vUrl']
            elif 'vurl' in each:
                webUrl = each['vurl']
            if 'aPicUrl' in each:
                poster = each['aPicUrl']
            elif 'vpic' in each:
                poster = each['vpic']
            if 'timeLength' in each:
                playLength = each['timeLength']
            if 'desc' in each:
                setIntro = each['desc']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = str(int(playLength)/60) + ':' + str(int(playLength)%60)
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = iqiyi_short_2()
    app.doProcess()