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


class all_youku_vipmovie():
    def __init__(self):
        print "Do spider all_youku_vipmovie."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = ["http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_1.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_1.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_2.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_3.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_4.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_5.html"
                         , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_6.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_7.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_8.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_9.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_10.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_11.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_12.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_13.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_14.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_15.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_16.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_17.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_18.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_19.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_20.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_21.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_22.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_23.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_24.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_25.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_26.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_27.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_28.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_29.html"
                         # , "http://list.youku.com/category/show/c_96_u_1_pt_2_s_6_d_1_p_30.html"
        ]
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.seqNocnt = 1
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_youku_vipmovie_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            seedList = []
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc)
            seed_P = soup.find("div", attrs={"class": "box-series"})
            if seed_P is not None:
                seedList = seed_P.find_all("div", attrs={"class": "p-thumb"})
            for each in seedList:
                vip_ticket = each.find('span', attrs={'class': 'vip-free'})
                if vip_ticket is not None:
                    if vip_ticket.get_text() == u'会员用券':
                        continue
                a_tag = each.find("a")
                if a_tag is not None:
                    subSeed = a_tag.get("href")
                    if subSeed is not None:
                        subSeed = "http:%s" % subSeed
                        self.seedList.append(subSeed)
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.program['pcUrl'] = seed
            self.firstSpider(seed)
            self.program["ptype"] = "电影".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = 1
            print self.program["name"],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
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
        point = 0.0
        poster = ""
        pcUrl = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        playLength = ""
        mainId = ""
        youkushootYear = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc)

        seed_v = re.search(r'http://v\.youku\.com/v_show/id_',seed)
        seed_Re = re.search(r'http://www\.youku\.com/show_page/id', seed)
        if seed_v:
            seed_P = soup.find('a', attrs={'class': 'desc-link'})
            if seed_P is not None:
                    seed = seed_P.get('href')
                    seed = "http:%s" % seed
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc)
        elif not seed_Re:
            seed_P = soup.find('h1', attrs={'class': 'title'})
            if seed_P is not None:
                seed_aTag = seed_P.find('a')
                if seed_aTag is not None:
                    seed = seed_aTag.get('href')
                    seed = "http:%s" % seed
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc)

        #pass the need vip ticket
        vip_ticket = soup.find('span', attrs={'class': 'vip-ticket'})
        if vip_ticket is not None:
            return

        poster_p = soup.find("div", attrs={'class': 'p-thumb'})
        if poster_p is not None:
            poster = poster_p.find('img').get("src")

        p_base_content = soup.find('div', attrs={'class': 'p-base'})
        if p_base_content is not None:
            for li in p_base_content.find_all('li'):
                li_p = str(li)
                if li.find('span', attrs={'class': 'star-num'}) is not None:
                    point = li.find('span', attrs={'class': 'star-num'}).get_text()
                elif li.get('class') == ['p-row', 'p-title']:
                    name_p = re.findall(r'/a>：(.*)<span'.decode('utf8'), li_p.decode('utf8'))
                    if name_p:
                        name = name_p[0]
                    if re.search(r'<'.decode('utf8'), name):
                        name_p = re.findall(r'(.*)<span'.decode('utf8'), name)
                        if name_p:
                            name = name_p[0]
                elif li.get('class') == ['p-alias']:
                    alias_p = li.get('title')
                elif li.find('span', attrs={'class': 'pub'}) is not None:
                    shootYear_P = li.find('span', attrs={'class': 'pub'})
                    if re.search(r'优酷'.decode('utf8'), li_p.decode('utf8')):
                        youkushootYear_text = re.findall(r'/label>(.*)</span', str(shootYear_P))
                        if youkushootYear_text:
                            youkushootYear_text = youkushootYear_text[0]
                            youkushootYear = ''.join(youkushootYear_text.split('-')[0])
                    else:
                        shootYear_text = re.findall(r'/label>(.*)</span', str(shootYear_P))
                        if shootYear_text:
                            shootYear_text = shootYear_text[0]
                            shootYear_data = shootYear_text.replace('-','')
                            # print(self.today, shootYear_data)
                            if shootYear_data > self.today:
                                return
                            shootYear = ''.join(shootYear_text.split('-')[0])
                elif re.search(r'<li>地区'.decode('utf8'), li_p.decode('utf8')):
                    area_p = li.get_text()
                    area_p = re.findall(r'地区：(.*)'.decode('utf8'), area_p)
                    if area_p:
                        area = area_p[0]
                        area = area.replace('/', ',')
                elif re.search(r'<li>类型'.decode('utf8'), li_p.decode('utf8')):
                    ctype_p = li.get_text()
                    ctype_p = re.findall(r'类型：(.*)'.decode('utf8'), ctype_p)
                    if ctype_p:
                        ctype = ctype_p[0]
                        ctype = ctype.replace('/', ',')
                elif re.search(r'<li>导演'.decode('utf8'), li_p.decode('utf8')):
                    director_p = li.get_text()
                    director_p = re.findall(r'导演：(.*)'.decode('utf8'), director_p)
                    if director_p:
                        director = director_p[0]
                elif li.get('class') == ['p-performer']:
                    star_list = []
                    for each in li.find_all('a'):
                        star_list.append(each.get_text())
                        star = ','.join(star_list)
                elif re.search(r'<li>总播放数'.decode('utf8'), li_p.decode('utf8')):
                    playTimesStr = li.get_text()
                    playTimesStr = re.findall(r'总播放数：(.*)'.decode('utf8'), playTimesStr)
                    if playTimesStr:
                        playTimesStr = playTimesStr[0]
                        playTimes_list = re.findall(r'(\d+)', playTimesStr)
                        playTimes = long(''.join(playTimes_list))
                elif li.get('class') == ['p-row', 'p-intro']:
                    intro = li.find('span').get_text().strip()
                else:
                    continue

            if shootYear == "":
                shootYear = youkushootYear

        if re.match(r'http://list\.youku\.com/show/id_(.+)\.html', seed):
            mainId = re.match(r'http://list\.youku\.com/show/id_(.+)\.html', seed).group(1)
        if re.match(r'http://v\.youku\.com/v_show/id_(.+)\.html', seed):
            mainId = re.match(r'http://v\.youku\.com/v_show/id_(.+)\.html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url', poster)
        self.program['star'] = spiderTool.listStringToJson('name', star)
        self.program['director'] = spiderTool.listStringToJson('name', director)
        self.program['ctype'] = spiderTool.listStringToJson('name', ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        self.secondSpider()

    def secondSpider(self):
            self.program_sub['setNumber'] = 1
            self.program_sub['setName'] = self.program["name"]
            self.program_sub['webUrl'] = self.program['pcUrl']
            if len(self.program['poster']) > 0:
                self.program_sub['poster'] = self.program['poster'][0]['url']
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = all_youku_vipmovie()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
