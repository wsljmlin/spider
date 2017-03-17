#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
import copy
import urllib
import urllib2
from spiderTool import spiderTool
from mediaContent import BASE_CONTENT
from mediaContent import PROGRAM_SUB
from bs4 import BeautifulSoup
from collections import OrderedDict


class all_renrenvideo_tv():
    def __init__(self):
        print "Do spider all_renrenvideo_tv."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedBase = [['USK',5],['JP', 5],['TH',5]]
        self.postseedurl = "http://api.rr.tv/v3plus/season/index"
        self.postdetailurl = " http://api.rr.tv/v3plus/season/detail"
        self.seedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.http_post_header={
		    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64)",
		    'clientVersion':"3.5.6",
		    'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_renrenvideo_tv_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def http_post(self, url, data, headers, retryTimes = 3):
        timeInterval = 8
        params = urllib.urlencode(data).encode(encoding='UTF8')
        doc = ""
        while doc == "" and retryTimes > 0:
            try:
                req = urllib2.Request(url, params, headers)
                r = urllib2.urlopen(req)
                doc = r.read()
            except:
                print "urllib2.HTTPError:Internal Server Error"
                retryTimes -= 1
                time.sleep(timeInterval)
        return doc

    def doProcess(self):
        for seed in self.seedBase:
            self.seedList = []
            area = seed[0]
            maxpagenum = seed[1]
            for page in range(maxpagenum):
                #compose post data
                postdata = {}
                postdata['rows'] = 10;
                postdata['page'] = page + 1;
                postdata['area'] = area;

                doc = self.http_post(self.postseedurl,postdata,self.http_post_header)
                try:
                    data = json.loads(doc, object_pairs_hook=OrderedDict)
                except:
                    continue

                #get baner
                if data.get('data').get('bannerTop'):
                    for item in data['data']['bannerTop']:
                        self.seedList.append(item['id'])

                #get other results
                if data.get('data').get('results'):
                    for item in data['data']['results']:
                        self.seedList.append(item['id'])
            self.seedSpider()

    def seedSpider(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "电视剧".decode("utf8")
            self.program['website'] = '人人视频'.decode("utf8")
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
        jsondata = {}

        postdata = {'seasonId':seed}
        doc = self.http_post(self.postdetailurl, postdata, self.http_post_header)
        try:
            data = json.loads(doc)
            # data = json.loads(doc, object_pairs_hook=OrderedDict)
        except:
            return

        mainId = seed;

        if data.get('data').get('season'):
            jsondata = data['data']['season']
            if jsondata.get('brief'):
                intro = jsondata['brief']
            if jsondata.get('actors'):
                actor_list = jsondata['actors']
                star_list = []
                for actor in actor_list:
                    star_list.append(actor['name'])
                star = ','.join(star_list)
            if jsondata.get('title'):
                name = jsondata['title']
            if jsondata.get('cover'):
                poster = jsondata['cover']
            if jsondata.get('cat'):
                ctype = jsondata['cat'].replace('/',',')
                ctype = ctype.replace(' ', '')


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro
        self.program['mainId'] = mainId

        if jsondata.get('playUrlList'):
            self.secondSpider(jsondata['playUrlList'])

    def secondSpider(self, video_list):
        video_list.sort(key=lambda k:(k.get('episode', 0)))
        for video in video_list:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ""

            webUrl = "renren://%s#%s" % (self.program['mainId'], video['episodeSid'])
            webUrl = urllib.quote(webUrl)
            setNumber = str(video['episode'])
            setName = str(setNumber)
            # print(webUrl, setNumber)

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == "" \
                    or setNumber is None or setName is None or webUrl is None:
                continue

            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)


if __name__ == '__main__':
    app = all_renrenvideo_tv()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()
