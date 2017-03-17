#!/usr/bin/env python
#encoding=UTF-8
import re
import sys
import json
import os
import time
from spiderTool import spiderTool
from bs4 import BeautifulSoup



class a_tmp_seed_spider():
    def __init__(self):
        print "Do spider a_tmp_seed_spider."

        self.seedList = []
        self.reSeedList = []
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "seed" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def seedSpider(self):
        for seed in self.seedList:
            self.firstSpider(seed)
        for seed in self.reSeedList:
            self.dataFile.write(seed + '\n')

    def firstSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        subSeed = ""
        title = ""

        titleTag = soup.find("h1", attrs={"class": "title"})
        if titleTag is not None:
            a_tag = titleTag.find("a")
            if a_tag is not None:
                subSeed = a_tag.get("href").encode('utf8')
                title = a_tag.get_text().encode('utf8')
        print title,subSeed, seed

        if subSeed is not None:
            self.reSeedList.append(subSeed)
        else:
            self.reSeedList.append("")


if __name__ == '__main__':
    app = a_tmp_seed_spider()
    if len(sys.argv) > 1:
        app.seedList = spiderTool.readSeedList(sys.argv[1])
        app.seedSpider()
    else:
        app.doProcess()