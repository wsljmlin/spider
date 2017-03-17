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
#XFUN吃货俱乐部
#春色无边搞笑盘点


class ablum_iqiyi_variety_1():
    def __init__(self):
        print "Do spider ablum_iqiyi_variety_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.seedList = ["http://www.iqiyi.com/a_19rrguentx.html"
                         ,"http://www.iqiyi.com/a_19rrguentx.html" #XFUN吃货俱乐部
                         ,'http://www.iqiyi.com/lib/m_208247014.html?src=search'#艾伦秀第13季
                         "http://www.iqiyi.com/a_19rrgjdzt1.html",#春色无边搞笑盘点
                         "http://www.iqiyi.com/a_19rrhal04x.html#vfrm=2-3-0-1", #十三亿分贝之一派方言
                         "http://www.iqiyi.com/a_19rrhanf9p.html", #咱们穿越吧第2季
                         "http://www.iqiyi.com/a_19rrhao8al.html"#星厨驾到第三季
                        ,'http://www.iqiyi.com/a_19rrhanya1.html#vfrm=2-3-0-1'#说出我的世界
                        ,'http://www.iqiyi.com/a_19rrhasbel.html#vfrm=2-3-0-1'#加油向未来
                        ,'http://www.iqiyi.com/a_19rrgu9s19.html#vfrm=2-3-0-1'#一呼柏应
                        ,'http://www.iqiyi.com/a_19rrgi7art.html#vfrm=2-3-0-1'#第一书记（2016）
                        ,'http://www.iqiyi.com/a_19rrgucd8p.html#vfrm=2-3-0-1'#幸福在哪里
                        ,'http://www.iqiyi.com/a_19rrgjahfl.html#vfrm=2-3-0-1'#我是大医生（2016）
                        ,'http://www.iqiyi.com/a_19rrh9rtx1.html'#今夜百乐门
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_iqiyi_variety_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "综艺".decode("utf8")
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

        poster_p = soup.find("img", attrs={'width': '195'})
        if poster_p is not None:
            poster = poster_p.get("src")
            name = poster_p.get("alt")

        starts_P = soup.find("dd", attrs={"class": "actor"})
        if starts_P is not None:
            start_list = []
            for each in starts_P.find_all('a'):
                start_list.append(each.get_text())
            star = ",".join(start_list)

        detail = soup.find("div", attrs={"class": "topic_item topic_item-rt"})
        if detail is not None:
            for div_p in detail.find_all("div",  attrs={"class": "item"}):
                for div in div_p:
                    if re.search("主持人：".decode("utf8"),each.get_text()):
                        director = each.get_text().split("主持人：".decode("utf8"))[1]
                    if re.search("类型：".decode("utf8"),each.get_text()):
                        ctype = each.get_text().split("类型：".decode("utf8"))[1]
                    if re.search("语言：".decode("utf8"),each.get_text()):
                        programLanguage = each.get_text().split("语言：".decode("utf8"))[1]

        content_p = soup.find('span',  attrs={"class":"showMoreText", "data-moreorless":"moreinfo", "style":"display: none;"})
        if content_p is not None:
            if content_p.find("span"):
                content_p = content_p.find("span")
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
    app = ablum_iqiyi_variety_1()
    app.doProcess()