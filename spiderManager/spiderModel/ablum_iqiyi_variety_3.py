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



class ablum_iqiyi_variety_3():
    def __init__(self):
        print "Do spider ablum_iqiyi_variety_3."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://www.iqiyi.com/lib/m_210446614.html'#姐姐好饿
                        , 'http://www.iqiyi.com/lib/m_210446614.html'#姐姐好饿
                        ,'http://www.iqiyi.com/lib/m_210483914.html'#撕人订制
                        ,'http://www.iqiyi.com/lib/m_210500114.html'#偶滴歌神啊
]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_iqiyi_variety_3_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
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
        pcUrl = ""
        poster = ""
        point = 0.0
        alias = ""
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""
        playLength = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        mainId_r = re.search(r'lib/(.*?)\.html'.decode('utf8'),seed)
        if mainId_r:
            mainId = mainId_r.group(1)

        poster_p = soup.find("div", attrs={'class': 'result_pic'})
        if poster_p is not None:
            poster_p_tag = poster_p.find('img')
            if poster_p_tag is not None:
                poster = poster_p_tag.get('src')
            name_p = poster_p.find('a')
            if name_p is not None:
                name = name_p.get('title')
                pcUrl = name_p.get('href')

        point_P = soup.find('span',attrs={'class': 'score_font'})
        if point_P is not None:
            point_r = re.search(r'\d+.\d+'.decode('utf8'), point_P.get_text())
            if point_r:
                point = point_r.group()

        detail = soup.find("div", attrs={"class": "result_detail"})
        if detail is not None:
            for p_tag in detail.find_all("div", attrs={"class": "topic_item clearfix"}):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("看点：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search(r"别名： 暂无".decode("utf8"),p_tag.get_text()) is not True \
                    and re.search(r"别名：(.*?)".decode("utf8"),p_tag.get_text()):
                    alias = re.search(r"别名：(.*?)".decode("utf8"),p_tag.get_text()).group(1)
                if re.search(r"上映时间：[^\\]*?(\d\d\d\d)".decode("utf8"), p_tag.get_text()):
                    shootYear = re.search(r"上映时间：[^\\]*?(\d\d\d\d)".decode("utf8"),p_tag.get_text()).group(1)
                if re.search(r"片长：[^\\]*?(\d+)".decode("utf8"),p_tag.get_text()):
                    playLength = re.search(r"片长：[^\\]*?(\d+)".decode("utf8"),p_tag.get_text()).group(1)


        content_p = soup.find('p',  attrs={"data-movlbshowmore-ele":"whole"})
        if content_p is not None:
                intro = content_p.get_text().strip()


        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program['pcUrl'] = pcUrl
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program["point"] = float(point)
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        self.program_sub['playLength'] = playLength + ':' + '00'

        seed_P = re.search(r'data-seriesdownload-aid="(?P<sourceId>\d+)"\s*data-seriesdownload-cid="(?P<cid>\d+)"', doc)
        if seed_P:
            sourceId = seed_P.group('sourceId')
            cid = seed_P.group('cid')
            self.program['mainId'] = sourceId
            seed_sub = 'http://cache.video.iqiyi.com/jp/sdvlst/%s/%s/' %(cid,sourceId)
            self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc.split('=')[1])
            data = json_data["data"]
        except:
            data = {}
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = each['tvYear']
            setName = each['videoName']
            webUrl = each['vUrl']
            poster = each['aPicUrl']
            playLength = each['timeLength']
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
    app = ablum_iqiyi_variety_3()
    app.doProcess()