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


class iqiyi_short_3():
    def __init__(self):
        print "Do spider iqiyi_short_3."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.seedList = [#"http://www.iqiyi.com/lib/m_209866614.html",#2、晚安，朋友圈 爱奇艺
                         "http://www.iqiyi.com/playlist295748402.html",#6、神剧亮了 爱奇艺###########
                         "http://www.iqiyi.com/playlist396149102.html",#17、笑不能停 爱奇艺@@@@@@@@@
        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "iqiyi_short_3_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '爱奇艺'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])
            print self.program['name'],self.program['totalSets']
            if self.program['name'] == '' or self.program['name'] is None \
                    or self.program['mainId'] == ''or self.program['mainId'] is None \
                    or self.program['totalSets'] < 1:
                continue
            content = {'program': self.program}
            str = json.dumps(content)
            self.dataFile.write(str + '\n')

    def firstSpider(self, seed):
        name = ""
        poster = ""
        maidId = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        name_p = soup.find('div', attrs={'class': 'bodanAlbum-msg-lt-pic fl'})
        if name_p is not None:
            name = name_p.find('a').get('title')
            if name_p.find('img') is not None:
                poster = name_p.find('img').get("src")

        maidId_re = re.search(r'com/(.*?)\.', seed)
        if maidId_re:
            maidId = maidId_re.group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['mainId'] = maidId
        pages = 0
        total_num_p = soup.find('li', attrs={'class': 'itemOne'})
        if total_num_p is not None:
            total_num_re = re.search(r'\d+', total_num_p.get_text())
            if total_num_re:
                total_num = total_num_re.group()
                pages = int(total_num)/20 + 2
        if pages != 0:
            for page in range(1,pages):
                sub_seed = seed.replace('.html', '-' + str(page) + '.html')
                self.secondSpider(sub_seed)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_pog = sub_soup.find_all("div", attrs={'class': 'site-piclist_pic'})
        for each in sub_pog:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            poster = ''
            setName = ""
            webUrl = ""
            playLength = ''

            poster_p = each.find('img')
            if poster_p is not None:
                poster = poster_p.get('src')
                setName = poster_p.get('title')
                setNumber_p = re.search(r'image/(\d+)/', poster)
                if setNumber_p:
                    setNumber = setNumber_p.group(1)

            webUrl_p = each.find('a')
            if webUrl_p is not None:
                webUrl = webUrl_p.get('href')

            playLength_p = each.find('span', attrs={'class': 'mod-listTitle_right'})
            if playLength_p is not None:
                playLength = playLength_p.get_text()

            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = playLength
            self.program['programSub'].append(self.program_sub)



if __name__ == '__main__':
    app = iqiyi_short_3()
    app.doProcess()