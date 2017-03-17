#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import types
import os
import time
import copy
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup


class mgtv_short_1():
    def __init__(self):
        print "Do spider mgtv_short_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://www.mgtv.com/v/6/101613/f/1094144.html"
,'http://www.mgtv.com/v/6/101613/f/1094144.html'#妹子说热剧
,'http://www.mgtv.com/v/6/158563/f/1777920.html'#小咖秀
,'http://www.mgtv.com/v/6/292430/f/3115009.html'#鲜炸社
,'http://www.mgtv.com/v/6/168030/f/1863425.html'#看够了没
,'http://www.mgtv.com/v/6/291965/f/3144194.html'#大咖头条
,'http://www.mgtv.com/v/6/291842/f/3012181.html'#混剪侠
,'http://www.mgtv.com/v/6/293477/f/3207951.html'#饭爱豆
,'http://www.mgtv.com/v/6/158354/f/2949121.html'#感觉自己萌萌哒
,'http://www.mgtv.com/v/6/292435/f/3172352.html'#天天打娱
,'http://www.mgtv.com/v/6/166144/f/3268355.html'#萌眼看重口
,'http://www.mgtv.com/v/6/168584/f/2931968.html'#哔哔娱乐秀
,'http://www.mgtv.com/v/6/167993/f/2973185.html'#马栏山牛人馆
,'http://www.mgtv.com/v/6/294063/f/3276032.html'#饭团私货朋友圈
,'http://www.mgtv.com/v/6/293394/f/3267841.html'#红人爱自拍
,'http://www.mgtv.com/v/6/167785/f/3143680.html'#马栏山剪刀手
,'http://www.mgtv.com/v/6/150882/f/2928653.html'#问题大了
,'http://www.mgtv.com/v/6/293268/f/3300386.html'#拐猫蜜
,'http://www.mgtv.com/v/8/157416/f/1740557.html'#女神TV
,'http://www.mgtv.com/v/6/155923/f/1755650.html'#萝莉侃剧
,'http://www.mgtv.com/v/6/292983/f/3300867.html'#笑死不偿命
,'http://www.mgtv.com/v/6/291094/f/3109397.html'#暴走看啥片儿第三季
,'http://www.mgtv.com/v/6/159440/f/2954242.html'#二更视频
,'http://www.mgtv.com/v/6/290272/f/3290851.html'#爱豆bibi社
,'http://www.mgtv.com/v/6/294171/f/3285505.html'#毒舌烧脑研究所

                         ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "mgtv_short_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '芒果TV'.decode("utf8")
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
        name = ""
        poster = ""
        point = 0.0
        shootYear = ""
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        pid = ""
        pid_P = re.search(r'http://www.mgtv.com/\w/\d+/(?P<mainId>\d+)/\w/(?P<pid>\d+)\.html', seed)
        if pid_P:
            pid = pid_P.group('pid')
            mainId = pid_P.group('mainId')

        seedJson = ""
        if pid != '':
            seedJson = 'http://m.api.hunantv.com/video/getbyid?videoId=%s' %(pid)
        else:
            return
        if mainId == "":
            mainId = pid

        doc = spiderTool.getHtmlBody(seedJson)
        if re.search(r'<html>', doc):
            doc = spiderTool.getHtmlBody(seedJson)
        json_data = json.loads(doc.strip())

        if json_data.has_key("data"):
            if type(json_data["data"]) is types.DictionaryType:
                json_data = json_data["data"]
                if json_data.has_key("detail"):
                    json_data = json_data["detail"]
                else:
                    return
            else:
                return

        if json_data.has_key("collectionName"):
            name = json_data["collectionName"]

        if json_data.has_key("image"):
            poster = json_data["image"]

        if json_data.has_key("year"):
            shootYear = json_data["year"]

        if json_data.has_key("director"):
            director_P = json_data["director"]
            if type(director_P) is types.UnicodeType:
                director = director_P.strip().replace(" / ",",")

        if json_data.has_key("player"):
            star_P = json_data["player"]
            if type(star_P) is types.UnicodeType:
                star = star_P.strip().replace(" / ",",")

        if json_data.has_key("area"):
            area_P = json_data["area"]
            if type(area_P) is types.UnicodeType:
                area = area_P.strip().replace(" ",",")

        if json_data.has_key('desc'):
            intro = json_data['desc']


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['point'] = point
        self.program['shootYear'] = shootYear
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        if json_data.has_key('typeId'):
            typeId = json_data['typeId']
        if json_data.has_key('collectionId'):
            collectionId = json_data['collectionId']

        pageNum = 20
        if json_data.has_key("totalvideocount"):
            pageNum = json_data["totalvideocount"]
        seed_sub = "http://m.api.hunantv.com/video/getListV2?videoId=%s&pageId=0&pageNum=%s"  %(pid, pageNum)
        self.secondSpider(seed_sub, seed, pid)
    def secondSpider(self, seed, seed_P, pid):
        data = []
        doc = spiderTool.getHtmlBody(seed)
        json_data = json.loads(doc)
        if json_data is not None:
            if json_data.has_key('data'):
                data_p = json_data['data']
                if type(data_p) is types.DictionaryType:
                    if data_p.has_key('list'):
                        data = data_p['list']
        if type(data) is not types.ListType:
            return

        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''
            playLength = ""
            setIntro = ""
            if type(each) is not types.DictionaryType:
                return
            if each.has_key('videoId'):
                videoId = str(each['videoId'])
                webUrl = seed_P.replace(pid, videoId)

            if each.has_key('videoIndex'):
                setNumber = str(each['videoIndex'])
            if setNumber == "" and len(data) == 1:
                setNumber = '1'
            if each.has_key('name'):
                setName = each['name']

            if each.has_key('image'):
                poster = each['image']

            if each.has_key('desc'):
                setIntro = each['desc']

            if each.has_key('time'):
                timeLength = each['time'].encode('utf8')
                playLength = str(int(timeLength) / 60) + ":" + str(int(timeLength) % 60)

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = mgtv_short_1()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()