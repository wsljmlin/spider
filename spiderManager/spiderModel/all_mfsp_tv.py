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


class all_mfsp_tv():
    def __init__(self):
        print "Do spider all_mfsp_tv."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = []
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_mfsp_tv_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def doProcess(self):
        for i in range(1, 2):
            self.seedBase.append("http://www.beevideo.tv/api/video2.0/video_list.action?pageNo=" + str(i) + "&pageSize=50&channelId=2")
        for seed in self.seedBase:
            seedList = []
            video_list = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            video_list_p = soup.find('video_list')
            if video_list_p is not None:
                video_list = video_list_p.find_all('video_item')
            for each in video_list:
                id = each.find('id')
                if id is not None:
                    id_num = id.get_text()
                    seed = 'http://www.beevideo.tv/api/video2.0/video_detail_info.action?videoId=' + id_num
                    seedList.append(seed)
            self.seedList = seedList
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '电视粉M'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            #print self.program['name'],self.program['totalSets']
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
        point = 0.0
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        if re.search(r'videoId=(?P<pid>\d+)', seed):
            mainId = re.search(r'videoId=(?P<pid>\d+)', seed).group('pid')

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        data = soup.find('video')
        if data is None:
            return


        name_p = data.find('name')
        name_r = re.search(r'<name>(.*?)</name>', doc)
        if name_p is not None:
            name = name_p.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif name_r:
            name = name_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        poster_p = data.find('smallImg')
        poster_r = re.search(r'<smallImg>(.*?)</smallImg>', doc)
        if poster_p is not None:
            poster = poster_p.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif poster_r:
            poster = poster_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        shootYear_P = data.find('screenTime')
        shootYear_r = re.search(r'<screenTime>(.*?)</screenTime>', doc)
        if shootYear_P is not None:
            shootYear = shootYear_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif shootYear_r:
            shootYear = shootYear_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        area_P = data.find('area')
        area_r = re.search(r'<area>(.*?)</area>', doc)
        if area_P is not None:
            area = area_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif area_r:
            area = area_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        director_P = data.find('director')
        director_r = re.search(r'<director>(.*?)</director>', doc)
        if director_P is not None:
            director = director_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif director_r:
            director = director_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        star_P = data.find('performer')
        star_r = re.search(r'<performer>(.*?)</performer>', doc)
        if star_P is not None:
            star = star_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif star_r:
            star = star_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        ctype_P = data.find('cate')
        ctype_r = re.search(r'<cate>(.*?)</cate>', doc)
        if ctype_P is not None:
            ctype = ctype_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif ctype_r:
            ctype = ctype_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()

        intro_P = data.find('annotation')
        intro_r =  re.search(r'<annotation>(.*?)</annotation>', doc)
        if intro_P is not None:
            intro = intro_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
        elif intro_r:
            intro = intro_r.group(1).replace('<![CDATA[', '').replace(']]>', '').strip()



        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['point'] = point
        self.program['shootYear'] = shootYear.split("-")[0]
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        detail_sub = data.find('videomergeinfolist')
        if detail_sub is not None:
            self.secondSpider(detail_sub)
    def secondSpider(self, detail_sub):
        data = detail_sub.find_all('videomergeinfo')
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            id = ""
            setNumber = ""
            setName = ""
            webUrl = ""
            id_P = each.find('id')
            if id_P is not None:
                id = id_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()
            if id != '':
                webUrl = 'http://www.beevideo.tv/api/video2.0/list_video_source_info.action?videoMergeInfoId=' + id
            setName_P = each.find('name')
            if setName_P is not None:
                setName = setName_P.get_text().replace('<![CDATA[', '').replace(']]>', '').strip()

            if re.search(r'20\d{6}', setName):
                setNumber = re.search(r'20\d{6}', setName).group()
            elif re.search(r'\d+$', setName):
                setNumber = re.search(r'\d+$', setName).group()
            elif re.search(r'第(\d+)集'.decode('utf8'), setName):
                setNumber = re.search(r'第(\d+)集'.decode('utf8'), setName).group(1)
            elif re.search(r'第([〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖貮两十拾百佰千仟万萬亿億兆]+)集'.decode('utf8'), setName):
                setNumberH = re.search(r'第([〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖貮两十拾百佰千仟万萬亿億兆]+)集'.decode('utf8'), setName).group(1)
                setNumber = spiderTool.cn2dig(setNumberH)
            elif len(data) == 1:
                setNumber = "1"
            else:
                setNumber = id
            if len(setNumber) > 7:
                setNumber = str(len(self.program['programSub']) + 1)

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_mfsp_tv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()