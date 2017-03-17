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


class youku_variety_1():
    def __init__(self):
        print "Do spider youku_variety_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB

        self.seedList = [
                        'http://list.youku.com/show/id_zcae79a088f5c11e5be16.html'#超哥找穿帮 2016]
                        ,'http://list.youku.com/show/id_z5ad3f29e07b511e6b2ad.html'#开心时刻与玩具介绍
                        ,'http://list.youku.com/show/id_z382ee5788dc611e5b692.html'#优酷全娱乐
                        ,'http://list.youku.com/show/id_zf9bb12323ef811e69b6d.html'#欢乐迪士尼
                        ,'http://list.youku.com/show/id_z978bf46e289b11e6abda.html'#搞笑蜘蛛侠
                        ,'http://list.youku.com/show/id_ze13b62e2047011e6b2ad.html'#极限大爆料
                        ,'http://list.youku.com/show/id_zb479d708be7911e5b522.html'#暴走法条君
                        ,'http://list.youku.com/show/id_z544934443efa11e6a080.html'#彩虹乐园
                        ,'http://list.youku.com/show/id_zb4cf061e1b4511e69e2a.html'#玩具大乐透
                        ,'http://list.youku.com/show/id_z8ac1a63e948711e38b3f.html'#青年电影院
                        ,'http://list.youku.com/show/id_z5cd51fc28e9411e5b2ad.html'#创食记
                        ,'http://list.youku.com/show/id_zb77de6d0bb5211e5b32f.html'#欢乐喜剧人来疯
                        ,'http://list.youku.com/show/id_z6571eeec3c2411e6abda.html'#电影笔记
                        ,'http://list.youku.com/show/id_zfa2fa2f6fc9411e5b522.html'#木东说
                        ,'http://list.youku.com/show/id_za69ea04e8f3711e5b2ad.html'#厨娘物语（2016）
                        ,'http://list.youku.com/show/id_za526429e941e11e5b432.html'#一条视频（2016）
                        ,'http://list.youku.com/show/id_z6ff61e7c8f5b11e5a080.html'#歪歌公社系列
                        ,'http://list.youku.com/show/id_z9e3056aeaf9a11e589e3.html'#逗鱼时刻
                        ,'http://list.youku.com/show/id_zcf6143aa8f5b11e5b522.html'#春色无边搞笑系列
                        ,'http://list.youku.com/show/id_z65a4f574ffe011e5b2ad.html'#生活家匠心之旅
                        ,'http://list.youku.com/show/id_z033f23c0270211e69e2a.html'#和潇洒姐塑身100天
                        ,'http://list.youku.com/show/id_za646cdfafc7511e583e8.html'#美食台
                        ,'http://list.youku.com/show/id_z18dabbf4280111e6abda.html'#环球梦游记
                        ,'http://list.youku.com/show/id_z44681bd293ea11e5b692.html'#微体兔
                        ,'http://list.youku.com/show/id_z341b70f88f5311e5b432.html'#yanyanfoodtube
                        ,'http://list.youku.com/show/id_zf1a86548df8c11e5b432.html'#微在涨知识
                        ,'http://list.youku.com/show/id_z6b876ec207b511e683e8.html'#姐妹美食与玩具
                        ,'http://list.youku.com/show/id_z5325feca07b511e683e8.html'#奇趣蛋惊喜蛋
                        ,'http://list.youku.com/show/id_z62d95cea93e311e59e2a.html'#电影供销社
                        ,'http://list.youku.com/show/id_z3d786b20a24411e5be16.html'#老烟斗鬼故事
                        ,'http://list.youku.com/show/id_zddfb21fe320f11e6a080.html'#装哔学院
                        ,'http://list.youku.com/show/id_z59289bfa1b2b11e683e8.html'#黄小趣街坊


        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "youku_variety_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            seed = seed.strip()
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "综艺".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
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

        seed_v = re.search(r'http://v\.youku\.com/v_show/id_', seed)
        seed_Re = re.search(r'http://www\.youku\.com/show_page/id', seed)
        if seed_v:
            seed_P = soup.find('a', attrs={'class': 'desc-link'})
            if seed_P is not None:
                seed = seed_P.get('href')
                seed = "http:%s" % seed
                doc = spiderTool.getHtmlBody(seed)
                soup = BeautifulSoup(doc, from_encoding="utf8")
        elif not seed_Re:
            seed_P = soup.find('h1', attrs={'class': 'title'})
            if seed_P is not None:
                seed_aTag = seed_P.find('a')
                if seed_aTag is not None:
                    seed = seed_aTag.get('href')
                    seed = "http:%s" % seed
                    doc = spiderTool.getHtmlBody(seed)
                    soup = BeautifulSoup(doc, from_encoding="utf8")

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
                elif li.find('span', attrs={'class': 'pub'}) is not None:
                    shootYear_P = li.find('span', attrs={'class': 'pub'})
                    shootYear_text = re.findall(r'/label>(.*)</span', str(shootYear_P))
                    if shootYear_text:
                        shootYear_text = shootYear_text[0]
                        shootYear = ''.join(shootYear_text.split('-')[0])
                elif re.search(r'<li>地区'.decode('utf8'), li_p.decode('utf8')):
                    area_p = re.findall(r'blank">(.*)</a'.decode('utf8'), li_p.decode('utf8'))
                    if area_p:
                        area = area_p[0]
                elif re.search(r'<li>类型'.decode('utf8'), li_p.decode('utf8')):
                    ctype_p = li.get_text()
                    ctype_p = re.findall(r'类型：(.*)'.decode('utf8'), ctype_p)
                    if ctype_p:
                        ctype_p = ctype_p[0]
                        ctype = ctype_p.replace('/', ',')
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

        if re.match(r'http://list\.youku\.com/show/(id_(.+))\.html', seed):
            mainId = re.match(r'http://list\.youku\.com/show/(id_(.+))\.html', seed).group(2)

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

        showid = ""
        showid_url = ""
        p_list_p = soup.find_all('script', attrs={'type': 'text/javascript'})
        if p_list_p is not None:
            for each in p_list_p:
                if re.search(r'PageConfig', str(each)):
                    showid_p = re.findall(r'showid:"(.*)", videoId', str(each))
                    if showid_p:
                        showid = showid_p[0]
                        showid_url = "http://list.youku.com/show/module?id=%s&tab=showInfo" % showid

        if showid_url != "":
            sub_doc = spiderTool.getHtmlBody(showid_url)
            try:
                data = json.loads(sub_doc)
            except:
                # print("load json error1111!")
                return
            if data.get('html') is None:
                # print("get html error1111")
                return

            sub_soup = BeautifulSoup(data['html'], from_encoding="utf8")
            reload_list_p = re.findall(r'id="reload_(\d+)"', data['html'])
            reload_list = list(set(reload_list_p))
            if reload_list:
                def numeric_compare(x, y):
                    x = int(x)
                    y = int(y)
                    if x > y:
                        return 1
                    elif x == y:
                        return 0
                    else:  # x<y
                        return -1

                reload_list.sort(numeric_compare)
                # print(reload_list)
                for reload in reload_list:
                    sub_seed = "http://list.youku.com/show/episode?id=%s&stage=reload_%s" % (mainId, reload)
                    #print(sub_seed)
                    self.secondSpider(sub_seed)


    def secondSpider(self, seed_sub):
        doc = spiderTool.getHtmlBody(seed_sub)
        try:
            data = json.loads(doc)
        except:
            # print("load json error22222!")
            return
        if data.get('html') is None:
            # print("get html error22222")
            return

        sub_soup = BeautifulSoup(data['html'], from_encoding="utf8")
        for li in sub_soup.find_all('li'):
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            playLength = ""
            setIntro = ""
            plot = []

            webUrl_p = li.find('a')
            if webUrl_p is not None:
                webUrl = "http://%s" % webUrl_p.get('href')
            setName_p = li.find('a')
            if setName_p is not None:
                setName = setName_p.get('title')
                if setName is None:
                    setName = setName_p.get_text()
            setNumber_p = li.find('dt')
            if setNumber_p is not None:
                setNumber = setNumber_p.get_text()

            if self.program['shootYear'] != "" and re.search(r'^\d{2}-\d{2}期$'.decode('utf8'), setNumber):
                setNumber = setNumber.replace("-", "")
                setNumber = self.program['shootYear'] + re.findall(r'(\d+)', setNumber)[0]
            elif re.search(r'\d{2}-\d{2}期'.decode('utf8'), setNumber):
                setNumber = setNumber.replace("-", "")
                setNumber = re.findall(r'(\d+)', setNumber)[0]
            elif re.search(r'\d+'.decode('utf8'), setNumber):
                setNumber = re.search(r'\d+'.decode('utf8'), setNumber).group(0)
            elif re.search(r'第(.*)期'.decode('utf8'), setNumber):
                setNumber = re.search(r'第(.*)期'.decode('utf8'), setNumber).group(0)
            elif re.search(r'第(.*)期'.decode('utf8'), setName):
                setNumber = re.search(r'第(.*)期'.decode('utf8'), setName).group(0)
            else:
                setNumber = ""

            if setNumber == "" and setName != "" and setName is not None and setNumber is not None:
                if re.search(r'\d+'.decode('utf8'), setName):
                    setNumber = re.search(r'\d+'.decode('utf8'), setName).group(0)

            if setNumber == "" or setName == "" or setNumber is None or setName is None or webUrl is None or webUrl == "" or \
                    re.search(r'预告'.decode('utf8'), setName):
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program_sub['plot'] = plot
            self.program['programSub'].append(self.program_sub)
            # print(self.program_sub)


if __name__ == '__main__':
    app = youku_variety_1()
    app.doProcess()