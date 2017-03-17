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
#陈真恋爱学


class youku_short_1():
    def __init__(self):
        print "Do spider youku_short_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://list.youku.com/show/id_za8ad878093ea11e5b692.html'
,"http://list.youku.com/show/id_z0a9d3a92032f11e48b3f.html"#唐唐脱口秀 第一季
,"http://list.youku.com/show/id_ze58f9a9c2cf511e4a705.html"#开心就好
,"http://list.youku.com/show/id_z2b2a0338e95111e28645.html"#成真恋爱学
,"http://list.youku.com/show/id_zfb1de8d28f2811e5be16.html"#托比恋爱学
,'http://list.youku.com/show/id_za8ad878093ea11e5b692.html'#许华升影视工作室系列 2016
,'http://list.youku.com/show/id_z75c7022ab83311e59e2a.html'#霸王别急眼 2016
,'http://list.youku.com/show/id_z52f919362be711e69e2a.html'#吴翠花
,'http://list.youku.com/show/id_z7801fd64a2f411e5a080.html'#尖叫制片厂 第二季
,'http://list.youku.com/show/id_z2076d8e8b33011e589e3.html'#笑打扮 2016
,'http://list.youku.com/show/id_z515f733026de11e6b432.html'#妹纸真会撩 2016
,'http://list.youku.com/show/id_za0cdb6ecbf4c11e59e2a.html'#马马虎虎 2016
,'http://list.youku.com/show/id_z13763d0eec0711e5b32f.html'#东北猫 2016
,'http://list.youku.com/show/id_z958e32f311d311e69c81.html'#尖叫影院 第二季
,'http://list.youku.com/show/id_z311a2c0891ad11e5b2ad.html'#精选几点整 2016
,'http://list.youku.com/show/id_zedbf8448bf1611e5b522.html'#papi酱 2016
,'http://list.youku.com/show/id_z4fffcdd2bb1a11e38b3f.html'#(牛人)Big笑工坊 第一季
,'http://list.youku.com/show/id_zefd780d4560511e5b2ad.html'#飞碟头条
,'http://list.youku.com/show/id_zb4620c988f5011e5be16.html'#极品街访 2016
,'http://list.youku.com/show/id_z01373c728f2f11e59e2a.html'#笑点研究所 2016
,'http://list.youku.com/show/id_zd5c211ba91af11e5a080.html'#陈翔六点半 2016
,'http://list.youku.com/show/id_zcf6143aa8f5b11e5b522.html'#春色无边搞笑系列 2016
,'http://list.youku.com/show/id_zbae522e88f3311e5be16.html'#摧绵大湿 2016
,'http://list.youku.com/show/id_zc2190160343811e6bdbb.html'#污妖王的笑容 2016
,'http://list.youku.com/show/id_z06271a8691a011e5b2ad.html'#萌眼看重口 2016
,'http://list.youku.com/show/id_z6b1f4f7606ad11e6b522.html'#电影贱客 2016
,'http://list.youku.com/show/id_z1b126af8321311e69c81.html'#JokeTV 街头恶搞和社会实验 2016
,'http://list.youku.com/show/id_z414f8d321b4811e6b432.html'#狗带劲趣点 2016
,'http://list.youku.com/show/id_z63fe7148f4b211e5b522.html'#神街访 2016
,'http://list.youku.com/show/id_z0aeca914b83d11e5b432.html'#谷阿莫说故事 第二季
,'http://list.youku.com/show/id_zf5b1e1c00f5111e5b5ce.html'#欧子直译 2015
,'http://list.youku.com/show/id_z11b62ef491bf11e5be16.html'#李韬爆笑生活 2016
,'http://list.youku.com/show/id_z1812cd24941811e5a080.html'#郑云工作室 2016
,'http://list.youku.com/show/id_ze11a862e91a411e5b2ad.html'#猿创精选 2016
,'http://list.youku.com/show/id_z37c14e0091ae11e5b432.html'#FUN滚吧 大哈 2016
,'http://list.youku.com/show/id_zdc851df493e811e5b522.html'#笑尿盘点 2016
,'http://list.youku.com/show/id_z8ce5cedc942011e5be16.html'#(牛人)YP脱口秀 2016
,'http://list.youku.com/show/id_za00ffad2efe211e583e8.html'#(牛人)飞碟一分钟 第二季
,'http://list.youku.com/show/id_z5d06fc5433c611e6b432.html'#(YIYI)搞笑配音系列短片 2016
,'http://list.youku.com/show/id_zccf9374233c711e6abda.html'#董新尧恶搞 2016
,'http://list.youku.com/show/id_zde11a072137511e69e2a.html'#桂林神街访 2016
,'http://list.youku.com/show/id_z871e989293ff11e5b2ad.html'#恶搞配音搞笑视频 2016
,'http://list.youku.com/show/id_zdf73234adaf011e5b32f.html'#十秒你就笑 2016
,'http://list.youku.com/show/id_z5bc3850a37e611e6b432.html'#威访 2016
,'http://list.youku.com/show/id_zd5bfe7f8af8411e589e3.html'#君笑坊创意配音 2016
,'http://list.youku.com/show/id_z98387714137611e6a080.html'#真晓声有理 2016
,'http://list.youku.com/show/id_zcf9a3748941811e5b522.html'#(牛人)咚哥唱谈 2016
,'http://list.youku.com/show/id_z9c7755e88f2811e5b2ad.html'#高铭脱口秀 2016
,'http://list.youku.com/show/id_z11b16cb0940411e59e2a.html'#有趣精选 2016
,'http://list.youku.com/show/id_z6ff61e7c8f5b11e5a080.html'#歪歌公社系列 2016
,'http://list.youku.com/show/id_za0426e20797911e5b2ad.html'#白想这么多
,'http://list.youku.com/show/id_z11681c8691a211e59e2a.html'#宽和茶园 2016
,'http://list.youku.com/show/id_z35b110aa33c911e6bdbb.html'#众乐为乐 2016
,'http://list.youku.com/show/id_z7e35d86e941b11e5b692.html'#(牛人)剑少兮创意作品 2016
,'http://list.youku.com/show/id_z3cd0c518ef3911e5b2ad.html'#Superviral TV 2016
,'http://list.youku.com/show/id_z50d35b2ada2611e5b522.html'#今晚曰不曰 2016
,'http://list.youku.com/show/id_z5be2024a294c11e59e2a.html'#男女那些事儿
,'http://list.youku.com/show/id_z595631be227911e6b32f.html'#欢乐治愈协会 2016
,'http://list.youku.com/show/id_za83f195b315511e6bdbb.html'#奥奥笑歌 2016
,'http://list.youku.com/show/id_zb2ecc4fc8f4111e5a080.html'#小操大吐槽 2016
,'http://list.youku.com/show/id_zd46576b691b111e59e2a.html'#逗比黑板报 2016
,'http://list.youku.com/show/id_z84591e1aaf8511e5b2ad.html'#深宅弃疗团 2016
,'http://list.youku.com/show/id_z6e6cfb4e348211e69e2a.html'#i乐y乐 2016
,'http://list.youku.com/show/id_z2e3808de227611e6b2ad.html'#浪小编的狗血生涯 2016
,'http://list.youku.com/show/id_z8e62209c344511e6b522.html'#人贱花开 2016
,'http://list.youku.com/show/id_ze9121216ad0c11e4b8e3.html'#西大那么大
,'http://list.youku.com/show/id_z6726719eab8f11e4b432.html'#陈瀚Siri
,'http://list.youku.com/show/id_zc32dd850dcfa11e4b692.html'#话题来了
,'http://list.youku.com/show/id_zd0529e2e940d11e5a080.html'#奇趣天下 2016
,'http://list.youku.com/show/id_z8ac1a63e948711e38b3f.html'#青年电影馆 第一季
,'http://list.youku.com/show/id_z69e131b8940e11e5a080.html'#明白学堂之明白看世界 2016
,'http://list.youku.com/show/id_zd1d4e744918c11e5a080.html'#小罗恶搞 2016
,'http://list.youku.com/show/id_z8d7df7682d3411e6abda.html'#文曰小强TalkShow 2016
,'http://list.youku.com/show/id_z281fbc023c2c11e59e2a.html'#小片片说大片 第一季
,'http://list.youku.com/show/id_z03acc7fc448911e4b2ad.html'#不要脸脱口秀 第一季
,'http://list.youku.com/show/id_z620833ae33d611e4b522.html'#女神有药 第一季
,'http://list.youku.com/show/id_z0e8f83fab90c11e5b522.html'#OMG!笑吧 第二季
,'http://list.youku.com/show/id_zb28a09fa11c511e6b432.html'#拉风的机长看大片 2016
,'http://list.youku.com/show/id_z0b84ab2e02e311e6b522.html'#高能路人 2016
,'http://list.youku.com/show/id_z284ebd2e91b111e5a080.html'#老式汽车 2016
,'http://list.youku.com/show/id_zb5c49a728db311e5b692.html'#糗事百科—小鸡炖蘑菇 第二季
,'http://list.youku.com/show/id_z7c2c8c96ceca11e4a080.html'#神奇的老皮 第一季
,'http://list.youku.com/show/id_zf77a5916ef1011e5b522.html'#大神有料 2016
,'http://list.youku.com/show/id_zd51e81a8dc6e11e5b432.html'#大学快跑 第二季
,'http://list.youku.com/show/id_z531f218e40c511e59e2a.html'#有梗 第一季
,'http://list.youku.com/show/id_z3101a1b091bc11e5b522.html'#女神TV 2016
,'http://list.youku.com/show/id_zce8916ea038511e59e2a.html'#二战那些事
,'http://list.youku.com/show/id_z36946c52079b11e69e2a.html'#粗大事啦 2016
,'http://list.youku.com/show/id_z31ed1868df8f11e5a2a2.html'#微在不懂爱 2016
,'http://list.youku.com/show/id_zeadc6954a5fd11e4b2ad.html'#混剪队长 第一季

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "youku_short_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '优酷'.decode("utf8")
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
        youkushootYear = ""

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
                elif li.get('class') == ['p-alias']:
                    alias = li.get('title')
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
        for ul in sub_soup.find_all('li'):
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""
            playLength = ""
            setIntro = ""
            plot = []

            webUrl_p = ul.find('a')
            if webUrl_p is not None:
                webUrl = "http://%s" % webUrl_p.get('href')
            setName_p = ul.find('a')
            if setName_p is not None:
                setName = setName_p.get_text()
            setNumber_p = ul.find('a')
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

if __name__ == '__main__':
    app = youku_short_1()
    app.doProcess()