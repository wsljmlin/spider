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

class ablum_qq_wdsj():
    def __init__(self):
        print "Do spider ablum_qq_wdsj."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = PROGRAM_SUB
        self.seedList = ['http://v.qq.com/vplus/xiaoben520/videos'#小本
                        ,'http://v.qq.com/vplus/xiaoben520/videos'#小本
                        ,'http://v.qq.com/vplus/chengzi233/videos'#大橙子
                        ,'http://v.qq.com/vplus/zhenshiqiguaile/videos'#真是奇怪了
                        ,'http://v.qq.com/vplus/maxkim0314/videos'#MaxKim
                        ,'http://v.qq.com/vplus/kamu/videos'#卡慕
                        ,'http://v.qq.com/vplus/yanhuang/videos'#炎黄
                        ,'http://v.qq.com/vplus/kaiqi/videos'#凯麒
                        ,'http://v.qq.com/vplus/xiaobaiMC/videos'#T-RO小白
                        ,'http://v.qq.com/vplus/moon/videos'#明月庄主
                        ,'http://v.qq.com/vplus/anyijun/videos'#安逸菌
                        ,'http://v.qq.com/vplus/xiaoxianjun/videos'#小贤菌
                        ,'http://v.qq.com/vplus/dahaitv/videos'#大海
                        ,'http://v.qq.com/vplus/youranxiaotian/videos'#悠然小天
                        ,'http://v.qq.com/vplus/pinkfish0319/videos'#粉鱼
                        ,'http://v.qq.com/vplus/tianluo/videos'#甜萝酱
                        ,'http://v.qq.com/vplus/xiaoA0v0/videos'#小A
                        ,'http://v.qq.com/vplus/biantao233/videos'#扁桃
                        ,'http://v.qq.com/vplus/fou4242/videos'#四二四儿
                        ,'http://v.qq.com/vplus/fuhao/videos'#负豪
                        ,'http://v.qq.com/vplus/qingyou/videos'#彼岸清幽
                        ,'http://v.qq.com/vplus/imaimu/videos'#叆霂
                        ,'http://v.qq.com/vplus/feixiongMC/videos'#飞熊TV我的世界
                        ,'http://v.qq.com/vplus/pika233/videos'#皮卡
                        ,'http://v.qq.com/vplus/xiaoyujun/videos'#小鱼

        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "ablum_qq_wdsj_" + self.today + ".txt")

    def __del__(self):
        if self.dataFile is not None:
            self.dataFile.close()

    def doProcess(self):
        for seed in self.seedList:
            self.program = copy.deepcopy(BASE_CONTENT["program"])
            self.firstSpider(seed)
            self.program['pcUrl'] = seed
            self.program["ptype"] = "游戏".decode("utf8")
            self.program['website'] = '腾讯'.decode("utf8")
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
        mainId = ""
        programNum = ''
        uniqueFlag = ''
        ctype = "我的世界".decode('utf8')

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        name_p = soup.find("span",attrs={'class':'txt', 'id':'userInfoNick'})
        if name_p is not None:
            name = name_p.get_text()
        self.program["name"] = spiderTool.changeName(name)

        mainId_p = re.search(r'http://v.qq.com/vplus/(.*?)/videos', seed)
        if mainId_p:
            mainId = mainId_p.group(1)
        self.program["mainId"] = mainId
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)

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

            setNumber_p = each.find('uploadtime')
            if setNumber_p is not None:
                setNumber = setNumber_p.get_text()
            setName_p = each.find("title")
            if setName_p is not None:
                setName = setName_p.get_text()
            webUrl_p = each.find("url")
            if webUrl_p is not None:
                webUrl = webUrl_p.get_text()
            poster_p = each.find('pic')
            if poster_p is not None:
                poster = poster_p.get_text()
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
    app = ablum_qq_wdsj()
    app.doProcess()