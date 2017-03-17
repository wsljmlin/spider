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
#你不知道的事

class qq_variety_1():
    def __init__(self):
        print "Do spider qq_variety_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://v.qq.com/vplus/nibuzhidaodeshi/videos"#你不知道的事
                       ,'http://v.qq.com/detail/5/50825.html'#美丽帮

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "qq_variety_1_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program['mainId'] = 'tvfan96258'
            self.program["ptype"] = "短视频".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
            self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.program['totalSets'] = len(self.program['programSub'])

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
        programNum = ''
        uniqueFlag = ''

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        name_p = soup.find("span",attrs={'class':'txt', 'id':'userInfoNick'})
        if name_p is not None:
            name = name_p.get_text()
        self.program["name"] = spiderTool.changeName(name)

        if re.search(r'共(\d+)个视频', doc):
            programNum = re.search(r'共(\d+)个视频', doc).group(1)
        if re.search(r"visited_euin : '(.*?)'", doc):
            uniqueFlag = re.search(r"visited_euin : '(.*?)'",doc).group(1)
        if programNum != '' and uniqueFlag != '':
            pages = range(1, int(programNum)/25 +2)
        else:
            return
        for page in pages:
            sub_url = 'http://c.v.qq.com/vchannelinfo?uin=%s&qm=1&pagenum=%s&num=25&sorttype=0&orderflag=1&callback=jQuery' %(uniqueFlag, page)
            self.secondSpider(sub_url)

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        sub_soup = BeautifulSoup(doc, from_encoding="utf8")
        sub_num = sub_soup.find_all("videolst")
        for each in sub_num:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ""
            setName = ""
            webUrl = ""
            poster = ''

            setNumber = each.find('uploadtime').get_text()
            setName = each.find("title").get_text()
            webUrl = each.find("url").get_text()
            poster = each.find('pic').get_text()
            if re.search(r'小时前'.decode('utf8'),setNumber):
                setNumber = time.strftime('%Y%m%d', time.localtime())
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace("-".decode('utf8'), "")
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = qq_variety_1()
    app.doProcess()