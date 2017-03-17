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
#优酷新闻


class all_youku_news():
    def __init__(self):
        print "Do spider all_youku_news."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ["http://list.youku.com/category/video/c_91_g_0_d_1_s_2_p_1.html",
                         "http://list.youku.com/category/video/c_91_g_0_d_1_s_2_p_2.html",
                         "http://list.youku.com/category/video/c_91_g_0_d_1_s_2_p_3.html",
                         "http://list.youku.com/category/video/c_91_g_0_d_1_s_2_p_4.html",
                         "http://list.youku.com/category/video/c_91_g_0_d_1_s_2_p_5.html"
                         ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        #self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "all_youku_news2_" + self.today + ".txt")

    #def __del__(self):
    #    if self.dataFile is not None:
    #        self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc)
            programs = soup.find_all('div', attrs={'class': 'yk-pack p-list'})
            for program in programs:
                self.firstSpider(program)

    def firstSpider(self, program):
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program["ptype"] = "新闻".decode("utf8")
        self.program['website'] = '优酷'.decode("utf8")
        self.program['getTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.program['totalSets'] = 1
        poster = ""
        name = ""
        mainId = ""
        pcUrl = ""

        poster_p = program.find("img")
        if poster_p is not None:
            poster = poster_p.get("src")
            name = poster_p.get("alt")

        pcUrl_P = program.find("a")
        if pcUrl_P is not None:
            pcUrl = "http:%s" % pcUrl_P.get("href")
        if re.search(r'id_(.*?)='.decode('utf8'), pcUrl):
            mainId = re.search(r'id_(.*?)='.decode('utf8'), pcUrl).group(1)

        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['pcUrl'] = pcUrl
        self.program['mainId'] = mainId
       	#print name,mainId,pcUrl,poster
        if self.program['name'] == '' or self.program['name'] is None \
                or self.program['mainId'] == ''or self.program['mainId'] is None:
            return

        json.dumps(PROGRAM_SUB)
        content = {'program': self.program}
        str = json.dumps(content)
        self.jsonData = str + "\n"
        #self.dataFile.write(str + '\n')

if __name__ == '__main__':
    app = all_youku_news()
    app.doProcess()
