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


class all_qq_cartoon():
    def __init__(self):
        print "Do spider all_qq_cartoon."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["https://v.qq.com/x/cartoonlist/?sort=5&offset=0",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=0",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=20",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=40",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=60",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=80",
                         "https://v.qq.com/x/cartoonlist/?sort=5&offset=100",
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.jsonData = ""
    #     self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_qq_cartoon_" + self.today + ".txt")
    #
    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            seed_P = soup.find("ul", attrs={"class": "figures_list"})
            if seed_P is not None:
                seedList = seed_P.find_all("li", attrs={"class": "list_item"})
            for each in seedList:
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        self.seedList.append(subSeed)
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            # seed_re = re.search(r'http://v.qq.com/cover/[\d\w]/(.*?)\.html', seed)
            seed_re = re.search(r'https://v.qq.com/[\d\w]/cover/(.*?)\.html', seed)
            if seed_re:
                maidId = seed_re.group(1)
                seed = 'https://v.qq.com/detail/%s/%s.html' % (maidId[0],maidId)
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "动漫".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            # print self.program['name'], self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue

            json.dumps(PROGRAM_SUB)
            content = {'program': self.program}
            str = json.dumps(content)
            self.jsonData = str + "\n"
            # self.dataFile.write(str + '\n')

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
        programLanguage = ""
        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("img",attrs={'itemprop':'image'})
        if poster_p is not None:
            if poster_p.get("src") is not None:
                poster = poster_p.get("src")
                poster = "http:%s" % poster
            if poster_p.get("alt") is not None:
                name = poster_p.get("alt")

        video_type = soup.find("div", attrs={"class": "video_type cf"})
        if video_type is not None:
            divs = video_type.find_all('div', attrs={"class": "type_item"})
            for div in divs:
                text = div.get_text()
                if re.search(r'地　区:'.decode("utf8"), text):
                    area_p = div.find('span', attrs={"class": "type_txt"})
                    if area_p is not None:
                        area = area_p.get_text()
                if re.search(r'语　言:'.decode("utf8"), text):
                    programLanguage_p = div.find('span', attrs={"class": "type_txt"})
                    if programLanguage_p is not None:
                        programLanguage = programLanguage_p.get_text()
                if re.search(r'上映时间:'.decode("utf8"), text):
                    shootYear_p = div.find('span', attrs={"class": "type_txt"})
                    if shootYear_p is not None:
                        shootYear = shootYear_p.get_text().split("-")[0]

        ctype_P = soup.find("div", attrs={"class": "tag_list"})
        if ctype_P is not None:
            ctype_list = []
            for each in ctype_P.find_all('a'):
                ctype_list.append(each.get_text())
            ctype = ",".join(ctype_list)

        person_p = soup.find("ul", attrs={"class": "actor_list cf"})
        if person_p is not None:
            lis = person_p.find_all('li')
            director_list = []
            star_list = []
            for li in lis:
                person = ""
                star_p = li.find("span", attrs={'class': 'name'})
                if star_p is not None:
                    person = star_p.get_text()
                if person != "" and  li.find("span", attrs={"class": "director"}):
                    director_list.append(person)
                elif person != "":
                    star_list.append(person)
            star = ",".join(star_list)
            director = ",".join(director_list)


        content_p = soup.find('span',  attrs={"class": "txt _desc_txt_lineHight"})
        if content_p is not None:
                intro = content_p.get_text().strip()

        if re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed):
            mainId = re.match(r'http://film\.qq\.com/(page|cover)/.*/(.*?).html',seed).group(2)
        if re.match(r'https://v\.qq\.com/detail/[\w\d]/(.*?).html', seed):
            mainId = re.match(r'https://v\.qq\.com/detail/[\w\d]/(.*?).html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['programLanguage'] = programLanguage
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        seed_sub = 'https://s.video.qq.com/loadplaylist?vkey=897_qqvideo_cpl_%s_qq' % mainId
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
            poster = ""

            setNumber_p = each.find_next_sibling("episode_number")
            if setNumber_p is not None:
                setNumber = setNumber_p.get_text()
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
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_qq_cartoon()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()