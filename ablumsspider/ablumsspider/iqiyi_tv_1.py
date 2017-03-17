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
#最好我们


class iqiyi_tv_1():
    def __init__(self):
        print "Do spider iqiyi_tv_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://www.iqiyi.com/a_19rrhbd6ad.html?vfm=2008_aldbd"
                        ,"http://www.iqiyi.com/a_19rrhbd6ad.html?vfm=2008_aldbd"#最好我们
                        ,"http://www.iqiyi.com/a_19rrhbeaxt.html?vfm=2008_aldbd"#老九门
                        ,"http://www.iqiyi.com/a_19rrh9oonl.html" #中国式关系
                        ,"http://www.iqiyi.com/a_19rrhaqkxp.html"#画江湖之不良人
                        ,"http://www.iqiyi.com/a_19rrh9rfup.html"#且行且珍行
                        ,"http://www.iqiyi.com/a_19rrh9pfpp.html"#宜昌保卫战
                        ,"http://www.iqiyi.com/a_19rrh9pu2p.html"#终极使命
                        ,"http://www.iqiyi.com/a_19rrhal739.html"#列刃
                        ,"http://www.iqiyi.com/a_19rrh9u5dh.html"#养个孩子不容易
                        ,"http://www.iqiyi.com/a_19rrhbe985.html"#怒火英雄
                        ,"http://www.iqiyi.com/a_19rrh9q55h.html"#安居
                        ,"http://www.iqiyi.com/a_19rrh9nldp.html"#女怕嫁错郎
                        ,"http://www.iqiyi.com/a_19rrh9pxgp.html"#麻辣律师团
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "iqiyi_tv_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
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

        poster_p = soup.find("ul", attrs={'class': 'focus_img_list'})
        if poster_p is not None:
            poster_p_sub = poster_p.find('li').get('style')
            if re.search(r'\((.*?)\)'.decode('utf8'), poster_p_sub):
                poster = re.search(r'\((.*?)\)'.decode('utf8'), poster_p_sub).group(1)

        name_p = soup.find('a', attrs={'class': 'white'})
        if name_p is not None:
            name = name_p.get_text()

        detail = soup.find("div", attrs={"class": "msg-hd-lt fl"})
        if detail is not None:
            for p_tag in detail.find_all("p"):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("主演：".decode("utf8"),p_tag.get_text()):
                    star = a_str


        content_p = soup.find('div',  attrs={"data-moreorless":"moreinfo"})
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

        seed_P = re.search(r'albumId:\s*(?P<albumId>\d+)[^\\]*?cid:\s*(?P<cid>\d+)'.decode('utf8'), doc)
        if seed_P:
            albumId = seed_P.group('albumId')
            cid = seed_P.group('cid')
            self.program['mainId'] = cid + "_" +albumId
            seed_sub = 'http://cache.video.iqiyi.com/jp/avlist/%s/' %(albumId)
            self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc.split('=')[1])
        data = json_data["data"]["vlist"]
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = each['pds']
            setName = each['vn']
            webUrl = each['vurl']
            poster = each['vpic']
            playLength = each['timeLength']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = str(int(playLength)/60) + ':' + str(int(playLength)%60)
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = iqiyi_tv_1()
    app.doProcess()