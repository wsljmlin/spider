#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
#重生之名流巨星


class qq_variety_2():
    def __init__(self):
        print "Do spider qq_variety_2."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://v.qq.com/detail/4/48461.html'
                        ,'http://v.qq.com/detail/4/48946.html'#派对之王
                        ,'http://v.qq.com/detail/4/44881.html'#故事中国周间版
                        ,'http://v.qq.com/detail/5/50538.html'#勇者大闯关
                        ,'http://v.qq.com/detail/4/49104.html'#陈辰全民星
                        ,'http://v.qq.com/detail/4/44428.html'#Oh My 思密达
                        ,'http://v.qq.com/detail/5/50341.html'#百家姓
                        ,'http://v.qq.com/detail/4/46460.html'#绿荫继承者
                        ,'http://v.qq.com/detail/4/44601.html'#西游奇遇记
                        ,'http://v.qq.com/detail/3/35691.html'#燃烧吧少年
                        ,'http://v.qq.com/detail/4/45170.html'#减出我人生
                        ,'http://v.qq.com/detail/4/49017.html'#燃卡100天
                        ,'http://v.qq.com/detail/4/48941.html'#杨澜访谈录
                        ,'http://v.qq.com/detail/4/48461.html'#来了就笑吧
                        ,'http://v.qq.com/detail/5/50825.html'#美丽帮
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "qq_variety_2_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        poster = ""
        star = ""
        director = ""
        ctype = ""
        shootYear = ""
        intro = ""
        mainId = ""
        area = ""
        name = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        detail = soup.find("div", attrs={"class": "mod_video_intro mod_video_intro_rich"})
        if detail is None:
            return

        poster_p = detail.find("img")
        if poster_p is not None:
            poster = poster_p.get("ll_src")



        name_p = detail.find("strong", attrs={"class": "title"})
        if name_p is not None:
                name =name_p.get_text()

        starts_P = detail.find("div", attrs={"class": "info_line cf"})
        if starts_P is not None:
            start_list = []
            for each in starts_P.find_all('a'):
                start_list.append(each.get_text())
            star = ",".join(start_list)

        ctype_P = detail.find("div", attrs={"class": "info_line info_line_tags cf"})
        if ctype_P is not None:
            ctype_list = []
            for each in ctype_P.find_all('a'):
                ctype_list.append(each.get_text())
            ctype = ",".join(ctype_list)

        content_p = soup.find('span',  attrs={"class": "desc"})
        if content_p is not None:
            intro = content_p.get_text()

        if re.match(r'http://v.qq.com/detail/\d/(\d+)\.html',seed):
            mainId = re.match(r'http://v.qq.com/detail/\d/(\d+)\.html',seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        if mainId != "":
            seed_sub = 'http://s.video.qq.com/loadplaylist?vkey=898_qqvideo_clpl_%s_qq&vtype=' % mainId
            self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("episode_number")
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""

            setNumber = each.get_text()
            setName_p = each.find_next_sibling("title")
            if setName_p is not None:
                setName = setName_p.get_text()
            setUrl_p = each.find_next_sibling("url")
            if setUrl_p is not None:
                webUrl = setUrl_p.get_text()
            poster_p = each.find_next_sibling("pic")
            if poster_p is not None:
                poster = poster_p.get_text()
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace("-".decode('utf8'), "")
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = qq_variety_2()
    app.doProcess()