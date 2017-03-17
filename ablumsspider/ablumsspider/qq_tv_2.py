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
#我的吸血鬼男友
#深井食堂


class qq_tv_2():
    def __init__(self):
        print "Do spider qq_tv_2."
        self.program = BASE_CONTENT["program"]
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://v.qq.com/detail/c/coftfal1pyf9581.html",
                         "http://v.qq.com/detail/q/qoudfsxphflt789.html",
                         "http://v.qq.com/detail/a/aoc0f4wxx0lagzg.html", #怒江之战
                         "http://v.qq.com/detail/i/in61eduxel9asc4.html", #大仙衙门
                         "http://v.qq.com/detail/l/lrwweimk8hanlk8.html", #我的奇妙男友
                         "http://v.qq.com/detail/b/brkpicg5l0q74rt.html", #超能姐姐大作战
                         "http://v.qq.com/detail/1/1qu8asbzxamls9n.html", #吉祥天宝
                         "http://v.qq.com/detail/d/df4fnnni5a95pjs.html", #昙花梦
                         "http://v.qq.com/detail/3/3d20hfxtawdq3d6.html",#多少爱可以重来

                        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "qq_tv_2_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['mainId'],self.program['name'],self.program['totalSets']
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

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("img",attrs={'itemprop':'image'})
        if poster_p is not None:
            poster = poster_p.get("ll_src")

        name_P = soup.find('div', attrs={'class': 'video_title'})
        if name_P is not None:
            name = name_P.find('strong').get_text()
            shootYear_P = name_P.find('span', attrs={'class': 'current_state'}).get_text()
            if re.search(r'\d+', shootYear_P):
                shootYear = re.search(r'\d+', shootYear_P).group()

        ctype_P = soup.find("div", attrs={"class": "info_tags"})
        if ctype_P is not None:
            ctype_list = []
            for each in ctype_P.find_all('a'):
                ctype_list.append(each.get_text())
            ctype = ",".join(ctype_list)

        star_P = soup.find("div", attrs={"class": "info_cast"})
        if star_P is not None:
            star_list = []
            for each in star_P.find_all('a'):
                star_list.append(each.get_text())
            star = ",".join(star_list)

        director_P = soup.find("div", attrs={"class": "info_director"})
        if director_P is not None:
            director_list = []
            for each in director_P.find_all('a'):
                director_list.append(each.get_text())
            director = ",".join(director_list)

        content_p = soup.find('span',  attrs={"class": "desc", 'itemprop': 'description'})
        if content_p is not None:
                intro = content_p.get_text().strip()

        if re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed):
            mainId = re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed).group(2)

        if re.match(r'http://v\.qq\.com/detail/[\w\d]/(.*?).html', seed):
            mainId = re.match(r'http://v\.qq\.com/detail/[\w\d]/(.*?).html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        seed_sub = 'http://s.video.qq.com/loadplaylist?vkey=897_qqvideo_cpl_%s_qq' % mainId
        self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("episode")
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""

            setNumber = each.get_text()
            setName = each.find_next_sibling("title").get_text()
            webUrl = each.find_next_sibling("url").get_text()
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = qq_tv_2()
    app.doProcess()