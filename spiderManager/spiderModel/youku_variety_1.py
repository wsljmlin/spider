#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
from spiderModel.spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class youku_variety_1():
    def __init__(self):
        print "Do spider youku_variety_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB

        self.seedList = ['http://www.youku.com/show_page/id_zcae79a088f5c11e5be16.html'
                        ,'http://www.youku.com/show_page/id_zcae79a088f5c11e5be16.html'#超哥找穿帮 2016]
                        ,'http://www.youku.com/show_page/id_zb479d708be7911e5b522.html'#暴走法条君
                        ,'http://www.youku.com/show_page/id_ze13b62e2047011e6b2ad.html'#极限大爆料
                        ,'http://www.youku.com/show_page/id_z5ad3f29e07b511e6b2ad.html'#开心时刻与玩具介绍
                        ,'http://www.youku.com/show_page/id_z382ee5788dc611e5b692.html'#优酷全娱乐
                        ,'http://www.youku.com/show_page/id_zf9bb12323ef811e69b6d.html'#欢乐迪士尼
                        ,'http://www.youku.com/show_page/id_z978bf46e289b11e6abda.html'#搞笑蜘蛛侠
                        ,'http://www.youku.com/show_page/id_z544934443efa11e6a080.html'#彩虹乐园
                        ,'http://www.youku.com/show_page/id_zb4cf061e1b4511e69e2a.html'#玩具大乐透
                        ,'http://www.youku.com/show_page/id_z8ac1a63e948711e38b3f.html'#青年电影院
                        ,'http://www.youku.com/show_page/id_z5cd51fc28e9411e5b2ad.html'#创食记
                        ,'http://www.youku.com/show_page/id_zb77de6d0bb5211e5b32f.html'#欢乐喜剧人来疯
                        ,'http://www.youku.com/show_page/id_z6571eeec3c2411e6abda.html'#电影笔记
                        ,'http://www.youku.com/show_page/id_zfa2fa2f6fc9411e5b522.html'#木东说
                        ,'http://www.youku.com/show_page/id_za69ea04e8f3711e5b2ad.html'#厨娘物语（2016）
                        ,'http://www.youku.com/show_page/id_za526429e941e11e5b432.html'#一条视频（2016）
                        ,'http://www.youku.com/show_page/id_z6ff61e7c8f5b11e5a080.html'#歪歌公社系列
                        ,'http://www.youku.com/show_page/id_z9e3056aeaf9a11e589e3.html'#逗鱼时刻
                        ,'http://www.youku.com/show_page/id_zcf6143aa8f5b11e5b522.html'#春色无边搞笑系列
                        ,'http://www.youku.com/show_page/id_z65a4f574ffe011e5b2ad.html'#生活家匠心之旅
                        ,'http://www.youku.com/show_page/id_z033f23c0270211e69e2a.html'#和潇洒姐塑身100天
                        ,'http://www.youku.com/show_page/id_za646cdfafc7511e583e8.html'#美食台
                        ,'http://www.youku.com/show_page/id_z18dabbf4280111e6abda.html'#环球梦游记
                        ,'http://www.youku.com/show_page/id_z44681bd293ea11e5b692.html'#微体兔
                        ,'http://www.youku.com/show_page/id_z341b70f88f5311e5b432.html'#yanyanfoodtube
                        ,'http://www.youku.com/show_page/id_zf1a86548df8c11e5b432.html'#微在涨知识
                        ,'http://www.youku.com/show_page/id_z6b876ec207b511e683e8.html'#姐妹美食与玩具
                        ,'http://www.youku.com/show_page/id_z5325feca07b511e683e8.html'#奇趣蛋惊喜蛋
                        ,'http://www.youku.com/show_page/id_z62d95cea93e311e59e2a.html'#电影供销社
                        ,'http://www.youku.com/show_page/id_z3d786b20a24411e5be16.html'#老烟斗鬼故事
                        ,'http://www.youku.com/show_page/id_zddfb21fe320f11e6a080.html'#装哔学院
                        ,'http://www.youku.com/show_page/id_z59289bfa1b2b11e683e8.html'#黄小趣街坊

        ]
        self.jsonData = ""
        # self.dataDir = '.' + os.path.sep + 'data'
        # self.today = time.strftime('%Y%m%d', time.localtime())
        # self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "youku_variety_1_" + self.today + ".txt")

    # def __del__(self):
    #     if self.dataFile is not None:
    #         self.dataFile.close()

    def seedSpider(self):
        for seed in self.seedList:
            seed = seed.strip()
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
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
        point = 0.0
        poster = ""
        name = ""
        shootYear = ""
        alias = ""
        area = ""
        star = ""
        director = ""
        ctype = ""
        playTimes = 0
        intro = ""
        mainId = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")
        seed_Re = re.search(r'http://www\.youku\.com/show_page/id', seed)
        if not seed_Re:
            seed_P = soup.find('h1', attrs={'class': 'title'})
            if seed_P is not None:
                seed_aTag = seed_P.find('a')
                if seed_aTag is not None:
                    seed = seed_aTag.get('href')
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc, from_encoding="utf8")

        point_P = soup.find('span',attrs={'class': 'rating'})
        if point_P is not None:
            if point_P.find('em',attrs={'class': 'num'}) is not None:
                point = point_P.find('em',attrs={'class': 'num'}).get_text()

        poster_p = soup.find("li",attrs={'class':'thumb'})
        if poster_p is not None:
            poster = poster_p.find('img').get("src")

        name_P = soup.find('h1', attrs={'class': 'title'})
        if name_P is not None:
            name_span = name_P.find('span', attrs={'class': 'name'})
            if name_span is not None:
                name = name_span.get_text()
            if re.search(r'\d{4}', name):
                shootYear = re.search(r'\d+', name).group()

        area_P = soup.find('span',attrs={'class': 'area'})
        if area_P is not None:
            area_list = []
            for each in area_P.find_all("a"):
                area_list.append(each.get_text())
            area = ",".join(area_list)

        ctype_all = soup.find_all("span", attrs={"class": "type"})
        for ctype_P in ctype_all:
            if re.search(r'类型:'.decode('utf8'), ctype_P.get_text()):
                ctype_list = []
                for each in ctype_P.find_all('a'):
                    ctype_list.append(each.get_text())
                ctype = ",".join(ctype_list)

        star_P = soup.find("span", attrs={"class": "actor"})
        if star_P is not None:
            star_list = []
            for each in star_P.find_all('a'):
                star_list.append(each.get_text())
            star = ",".join(star_list)

        director_P = soup.find("span", attrs={"class": "director"})
        if director_P is not None:
            director_list = []
            for each in director_P.find_all('a'):
                director_list.append(each.get_text())
            director = ",".join(director_list)

        playTimes_P = soup.find('span', attrs={'class': 'play'})
        if playTimes_P is not None:
            playTimesStr = playTimes_P.get_text()
            playTimes_list = re.findall(r'(\d+)', playTimesStr)
            playTimes = long(''.join(playTimes_list))

        content_p = soup.find('span',  attrs={"class": "short", 'id': 'show_info_short'})
        if content_p is not None:
                intro = content_p.get_text().strip()

        if re.match(r'http://www\.youku\.com/show_page/(id_(\w+))\.html', seed):
            mainId = re.match(r'http://www\.youku\.com/show_page/id_(\w+)\.html', seed).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program["alias"] = spiderTool.changeName(alias)
        self.program["point"] = float(point)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['shootYear'] = shootYear
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['playTimes'] = long(playTimes)
        self.program['intro'] = intro
        self.program['mainId'] = mainId
        urlList = re.findall(r'<li\s+data="(reload_\d+)"\s*(class="current"){0,1}\s*>', doc)
        if urlList:
                for url in urlList:
                    seed_sub = 'http://www.youku.com/show_episode/id_%s.html?dt=json&divid=%s' % (mainId, url[0])
                    self.secondSpider(seed_sub)
        else:
                seed_sub = 'http://www.youku.com/show_episode_id_%s.html?dt=json' % mainId
                self.secondSpider(seed_sub)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("ul", attrs={'class': 'item'})
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            stars = ""

            setName_P = each.find('li')
            if setName_P is not None:
                a_tag = setName_P.find("a")
                if a_tag is not None:
                    setName = a_tag.get('title')
                    webUrl = a_tag.get('href')
                label_tag = setName_P.find("label")
                if label_tag is not None:
                    num_tag = label_tag.get_text().strip()
                    if self.program['shootYear'] != "" and re.search(r'^\d{2}-\d{2}期$'.decode('utf8'), num_tag):
                        setNumber = self.program['shootYear'] + num_tag.replace("-","").replace("期".decode('utf8'), "")
                    elif re.search(r'^\d{2}-\d{2}期$'.decode('utf8'), num_tag):
                        year = time.strftime('%y', time.localtime())
                        if re.search(r'reload_(20\d{2})',seed):
                            setNumber = re.search(r'reload_(20\d{2})', seed).group(1) + num_tag.replace("-","").replace("期".decode('utf8'), "")
                        elif re.search(year, setName):
                            setNumber = time.strftime('%Y', time.localtime()) + num_tag.replace("-","").replace("期".decode('utf8'), "")
                    elif re.search(r'\d+'.decode('utf8'), num_tag):
                        setNumber = re.search(r'\d+'.decode('utf8'), num_tag).group()
                    else:
                        setNumber = ""
            stars_P = each.find('li', attrs={'class': 'iguests'})
            if stars_P is not None:
                starsList = []

                a_tag = stars_P.find_all("a")
                for a in a_tag:
                    if a.get_text() is not None:
                        starsList.append(a.get_text().strip())
                stars = ",".join(starsList)

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['stars'] = stars
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = youku_variety_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()