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


class iqiyi_short_1():
    def __init__(self):
        print "Do spider iqiyi_short_1."
        self.program = copy.deepcopy(BASE_CONTENT["program"])
        self.program_sub = copy.deepcopy(PROGRAM_SUB)
        self.seedList = [#"http://www.iqiyi.com/a_19rrgued6t.html",#1笑霸来了-----------------------
'http://www.iqiyi.com/a_19rrhb42qd.html'
,'http://www.iqiyi.com/a_19rrhb42qd.html'#so问题来了
,'http://www.iqiyi.com/a_19rrhak5cl.html'#阿福来了
,'http://www.iqiyi.com/a_19rrhb4mfl.html'#畅姐哔哔哔
,'http://www.iqiyi.com/a_19rrhaiipl.html'#软软の秀
,'http://www.iqiyi.com/a_19rrhax471.html'#绅士大概一分钟
,'http://www.iqiyi.com/a_19rrhairf9.html'#内涵神评论
,'http://www.iqiyi.com/a_19rrhb9cw1.html'#星知奇趣新闻
,'http://www.iqiyi.com/a_19rrhbezjd.html'#哔哔嘿嘿乐
,'http://www.iqiyi.com/a_19rrhajvyl.html'#关八热话题
,'http://www.iqiyi.com/a_19rrhb7j0t.html'#娱乐有机物
,'http://www.iqiyi.com/a_19rrhbh55x.html'#大咖笑料
,'http://www.iqiyi.com/a_19rrhajl3p.html'#作死歪果仁
,'http://www.iqiyi.com/a_19rrhbbq5t.html#vfrm=2-3-0-1'#大咖都穿了
,'http://www.iqiyi.com/a_19rrhbgert.html#vfrm=2-3-0-1'#我叫白胖子
,'http://www.iqiyi.com/a_19rrhalnnl.html#vfrm=2-3-0-1'#咔梦秀场
,'http://www.iqiyi.com/a_19rrhahiot.html#vfrm=2-3-0-1'#胡椒黄了爆笑小视频
,'http://www.iqiyi.com/a_19rrhbgpf5.html#vfrm=2-3-0-1'#搞笑整人节目
,'http://www.iqiyi.com/a_19rrhb7xzp.html#vfrm=2-3-0-1'#网罗天下
,'http://www.iqiyi.com/a_19rrhajrrp.html#vfrm=2-3-0-1'#奇葩大本营
,'http://www.iqiyi.com/a_19rrgj9m35.html#vfrm=2-3-0-1'#郑云工作室
,'http://www.iqiyi.com/a_19rrhajnjh.html'#胥渡吧神配音 第六季
,'http://www.iqiyi.com/a_19rrhb4ulx.html#vfrm=2-3-0-1'#摧绵大湿搞笑盘点
,'http://www.iqiyi.com/a_19rrhal19p.html#vfrm=2-3-0-1'#奇闻异录
,'http://www.iqiyi.com/a_19rrhadjnd.html#vfrm=2-3-0-1'#喜闻乐溅
,'http://www.iqiyi.com/a_19rrhb4cu9.html#vfrm=2-3-0-1'#大咖剧星(搞笑)
,'http://www.iqiyi.com/a_19rrhbe2gd.html#vfrm=2-3-0-1'#柚子木字幕组·搞笑娱乐
,'http://www.iqiyi.com/a_19rrhb7ubd.html#vfrm=2-3-0-1'#十分开心
,'http://www.iqiyi.com/a_19rrhb8p9t.html#vfrm=2-3-0-1'#头条乱炖
,'http://www.iqiyi.com/a_19rrhawnsx.html#vfrm=2-3-0-1'#一风之音《恶了就搞》
,'http://www.iqiyi.com/a_19rrhadjj1.html#vfrm=2-3-0-1'#人生赢家
,'http://www.iqiyi.com/a_19rrhb1rr5.html#vfrm=2-3-0-1'#一周热播榜
,'http://www.iqiyi.com/a_19rrhab3ix.html#vfrm=2-3-0-1'#(FACEBEAR)呼你熊脸
,'http://www.iqiyi.com/a_19rrhahjud.html#vfrm=2-3-0-1'#节操补习班
,'http://www.iqiyi.com/a_19rrhbh3fp.html#vfrm=2-3-0-1'#搞笑萌宠
,'http://www.iqiyi.com/a_19rrhbb0zx.html#vfrm=2-3-0-1'#奇闻囧事一箩筐
,'http://www.iqiyi.com/a_19rrhb5749.html#vfrm=2-3-0-1'#大话娱乐圈(搞笑)
,'http://www.iqiyi.com/a_19rrhammr1.html#vfrm=2-3-0-1'#耐撕男女
,'http://www.iqiyi.com/a_19rrgibi2p.html#vfrm=2-3-0-1'#Big笑工坊
,'http://www.iqiyi.com/a_19rrham1l5.html#vfrm=2-3-0-1'#西施叨叨叨 第二季
,'http://www.iqiyi.com/a_19rrhap14p.html#vfrm=2-3-0-1'#8090你老了
,'http://www.iqiyi.com/a_19rrhbgabt.html#vfrm=2-3-0-1'#印象精选
,'http://www.iqiyi.com/a_19rrhamu79.html#vfrm=2-3-0-1'#街头老司机
,'http://www.iqiyi.com/a_19rrhabdzh.html#vfrm=2-3-0-1'#(FACEBEAR)萌你一脸
,'http://www.iqiyi.com/a_19rrhajc0x.html#vfrm=2-3-0-1'#bibi娱乐社
,'http://www.iqiyi.com/a_19rrhb5rzl.html#vfrm=2-3-0-1'#VitalyzdTV
,'http://www.iqiyi.com/a_19rrhai4a9.html#vfrm=2-3-0-1'#星扒客
,'http://www.iqiyi.com/a_19rrhaf9v5.html#vfrm=2-3-0-1'#(老美一分钟)第二季
,'http://www.iqiyi.com/a_19rrhbck6p.html#vfrm=2-3-0-1'#葱哥大视野
,'http://www.iqiyi.com/a_19rrhafy1x.html#vfrm=2-3-0-1'#学妹来也
,'http://www.iqiyi.com/a_19rrhaj8lt.html#vfrm=2-3-0-1'#衰神驾到
,'http://www.iqiyi.com/a_19rrhb3io9.html#vfrm=2-3-0-1'#一见你就笑
,'http://www.iqiyi.com/a_19rrhb6y7h.html#vfrm=2-3-0-1'#大咖爆料
,'http://www.iqiyi.com/a_19rrhbd2ut.html#vfrm=2-3-0-1'#印象谈唱
,'http://www.iqiyi.com/a_19rrhama6h.html#vfrm=2-3-0-1'#刘老师带你飞
,'http://www.iqiyi.com/a_19rrhai6fx.html#vfrm=2-3-0-1'#OMG!有老外
,'http://www.iqiyi.com/a_19rrgiaq8t.html#vfrm=2-3-0-1'#唐纳德在中国
,'http://www.iqiyi.com/a_19rrhalvwd.html#vfrm=2-3-0-1'#学妹娱乐
,'http://www.iqiyi.com/a_19rrhai59d.html#vfrm=2-3-0-1'#老外不老外
,'http://www.iqiyi.com/a_19rrhb8dv1.html#vfrm=2-3-0-1'#陕一二七
,'http://www.iqiyi.com/a_19rrhaahs9.html#vfrm=2-3-0-1'#火龙果的日常
,'http://www.iqiyi.com/a_19rrhanpml.html#vfrm=2-3-0-1'#不可能这么鬼畜
,'http://www.iqiyi.com/a_19rrhb9md1.html#vfrm=2-3-0-1'#Superviral Cute
,'http://www.iqiyi.com/a_19rrhb6qdh.html#vfrm=2-3-0-1'#会玩
,'http://www.iqiyi.com/a_19rrhalyw1.html#vfrm=2-3-0-1'#《疯狂料理》第一季
,'http://www.iqiyi.com/a_19rrhamcah.html#vfrm=2-3-0-1'#233吐槽团
,'http://www.iqiyi.com/a_19rrhait6h.html#vfrm=2-3-0-1'#大呲花 第一季
,'http://www.iqiyi.com/a_19rrhbaugx.html#vfrm=2-3-0-1'#闻闻说
,'http://www.iqiyi.com/a_19rrhb03ap.html#vfrm=2-3-0-1'#笑里藏道第一季
,'http://www.iqiyi.com/a_19rrhc44bl.html#vfrm=2-3-0-1'#90后暴走夫妻
,'http://www.iqiyi.com/a_19rrhb4vl5.html#vfrm=2-3-0-1'#海南扒一扒
,'http://www.iqiyi.com/a_19rrhai87l.html#vfrm=2-3-0-1'#王小贱神吐槽
,'http://www.iqiyi.com/a_19rrhb9ma9.html#vfrm=2-3-0-1'#Superviral Emotion
,'http://www.iqiyi.com/a_19rrhbgk6h.html#vfrm=2-3-0-1'#一万个不相信
,'http://www.iqiyi.com/a_19rrhbyxpp.html#vfrm=2-3-0-1'#娱人榜
,'http://www.iqiyi.com/a_19rrhakxr1.html#vfrm=2-3-0-1'#全民精选
,'http://www.iqiyi.com/a_19rrhb5jz5.html#vfrm=2-3-0-1'#笑打扮
,'http://www.iqiyi.com/a_19rrhagmcx.html#vfrm=2-3-0-1'#大咖撸星座
,'http://www.iqiyi.com/a_19rrgj9u2l.html#vfrm=2-3-0-1'#中国笑话王
,'http://www.iqiyi.com/a_19rrhali1h.html#vfrm=2-3-0-1'#音乐小嘿污
,'http://www.iqiyi.com/a_19rrgi7qsx.html#vfrm=2-3-0-1'#2B青年欢乐多
,'http://www.iqiyi.com/a_19rrhc419h.html#vfrm=2-3-0-1'#有样儿(达人)
,'http://www.iqiyi.com/a_19rrhamodp.html#vfrm=2-3-0-1'#电影天下第二季
,'http://www.iqiyi.com/a_19rrhb9gj9.html#vfrm=2-3-0-1'#知了读书
,'http://www.iqiyi.com/a_19rrhavimx.html#vfrm=2-3-0-1'#凯家班创意配音
,'http://www.iqiyi.com/a_19rrhajxyl.html#vfrm=2-3-0-1'#OMG!问东西
,'http://www.iqiyi.com/a_19rrgj9k99.html#vfrm=2-3-0-1'#剑少兮合集
,'http://www.iqiyi.com/a_19rrhbh7fx.html#vfrm=2-3-0-1'#最佳原创
,'http://www.iqiyi.com/a_19rrha9fox.html#vfrm=2-3-0-1'#宇宙大新闻
,'http://www.iqiyi.com/a_19rrhad001.html#vfrm=2-3-0-1'#上班狗日爆
,'http://www.iqiyi.com/a_19rrhahg59.html#vfrm=2-3-0-1'#朕!真来了
,'http://www.iqiyi.com/a_19rrhbgpf5.html#vfrm=2-3-0-1'#搞笑整人节目
,'http://www.iqiyi.com/a_19rrhb6cg5.html#vfrm=2-3-0-1'#笑料百出精选
,'http://www.iqiyi.com/a_19rrhaillp.html#vfrm=2-3-0-1'#高亮乐翻天
,'http://www.iqiyi.com/a_19rrginhed.html#vfrm=2-3-0-1'#扒神嗨评
,'http://www.iqiyi.com/a_19rrhbd1wl.html#vfrm=2-3-0-1'#搞笑小广告
,'http://www.iqiyi.com/a_19rrhag9tp.html#vfrm=2-3-0-1'#有你冇我
,'http://www.iqiyi.com/a_19rrhaiygx.html#vfrm=2-3-0-1'#嘻出望外
,'http://www.iqiyi.com/a_19rrhb8xol.html#vfrm=2-3-0-1'#别闹了
,'http://www.iqiyi.com/a_19rrhahxhh.html#vfrm=2-3-0-1'#逗吧三人组车振篇
,'http://www.iqiyi.com/a_19rrhaml39.html#vfrm=2-3-0-1'#一个喜剧
,'http://www.iqiyi.com/a_19rrhbcszx.html#vfrm=2-3-0-1'#酋长BB秀
,'http://www.iqiyi.com/a_19rrhaga61.html#vfrm=2-3-0-1'#前列先发言
,'http://www.iqiyi.com/a_19rrhaah8t.html#vfrm=2-3-0-1'#哔哔剧有趣(搞笑)
,'http://www.iqiyi.com/a_19rrhb7olt.html#vfrm=2-3-0-1'#国闻趣事
,'http://www.iqiyi.com/a_19rrginhed.html#vfrm=2-3-0-1'#扒神嗨评
,'http://www.iqiyi.com/a_19rrhb1p75.html#vfrm=2-3-0-1'#路边社
,'http://www.iqiyi.com/a_19rrhae8kp.html#vfrm=2-3-0-1'#Fans堂最有Fun之胡七八说
,'http://www.iqiyi.com/a_19rrhb6hc1.html#vfrm=2-3-0-1'#FUN滚吧大哈
,'http://www.iqiyi.com/a_19rrhb07p5.html#vfrm=2-3-0-1'#歪歌社团(创意视频)
,'http://www.iqiyi.com/a_19rrhba6tl.html#vfrm=2-3-0-1'#君笑工坊创意配音
,'http://www.iqiyi.com/a_19rrhapjeh.html#vfrm=2-3-0-1'#心灵乌鸡汤
,'http://www.iqiyi.com/a_19rrhavrpl.html#vfrm=2-3-0-1'#酷客春季恶作剧
,'http://www.iqiyi.com/a_19rrhaja9l.html#vfrm=2-3-0-1'#尼美快报
,'http://www.iqiyi.com/a_19rrhbe2gd.html#vfrm=2-3-0-1'#柚子木字幕组·搞笑娱乐


        ]
        self.dataDir = '.' + os.path.sep + 'data'
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.dataFile = spiderTool.openFile(self.dataDir + os.path.sep + "iqiyi_short_1_" + self.today + ".txt")

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
            print self.program['name'], self.program['totalSets']
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
        star = ""
        director = ""
        ctype = ""
        programLanguage = ""
        intro = ""
        mainId = ""
        area = ""

        doc = spiderTool.getHtmlBody(seed)
        soup = BeautifulSoup(doc, from_encoding="utf8")

        poster_p = soup.find("img", attrs={'width': '195'})
        if poster_p is not None:
            poster = poster_p.get("src")
            name = poster_p.get("alt")

        starts_P = soup.find("dd", attrs={"class": "actor"})
        if starts_P is not None:
            start_list = []
            for each in starts_P.find_all('a'):
                start_list.append(each.get_text())
            star = ",".join(start_list)

        detail = soup.find_all("div", attrs={"class": "topic_item clearfix"})
        for each in detail:
            for p_tag in each.find_all('em'):
                a_list = []
                for a_tag in p_tag.find_all('a'):
                    a_list.append(a_tag.get_text())
                a_str = ','.join(a_list)
                if re.search("导演：".decode("utf8"),p_tag.get_text()):
                    director = a_str
                if re.search("语言：".decode("utf8"),p_tag.get_text()):
                    programLanguage = a_str
                if re.search("配音：".decode("utf8"),p_tag.get_text()):
                    star = a_str
                if re.search("地区：".decode("utf8"),p_tag.get_text()):
                    area = a_str
                if re.search("类型：".decode("utf8"),p_tag.get_text()):
                    ctype = a_str


        content_p = soup.find('span',  attrs={"class":"showMoreText", "data-moreorless":"moreinfo", "style":"display: none;"})
        if content_p is not None:
            if content_p.find("span"):
                content_p = content_p.find("span")
            if re.search("简介：".decode("utf8"),content_p.get_text()):
                intro = content_p.get_text().split("简介：".decode("utf8"))[1].strip()


        self.program["name"] = spiderTool.changeName(name)
        self.program['poster'] = spiderTool.listStringToJson('url',poster)
        self.program['star'] = spiderTool.listStringToJson('name',star)
        self.program['director'] = spiderTool.listStringToJson('name',director)
        self.program['ctype'] = spiderTool.listStringToJson('name',ctype)
        self.program['programLanguage'] = programLanguage
        self.program['area'] = spiderTool.listStringToJson('name', area)
        self.program['intro'] = intro

        seed_P = re.search(r'sourceId:\s*(?P<sourceId>\d+),\s*cid:\s*(?P<cid>\d+)', doc)
        if seed_P:
            sourceId = seed_P.group('sourceId')
            cid = seed_P.group('cid')
            self.program['mainId'] = sourceId
            if sourceId != '0':
                seed_sub = 'http://cache.video.iqiyi.com/jp/sdvlst/%s/%s/' %(cid,sourceId)
                self.secondSpider(seed_sub)
                return

        seed_P =  re.search(r'albumId:\s*(?P<albumId>\d+),[^\\]*?cid:\s*(?P<cid>\d+)', doc)
        if seed_P:
            albumId = seed_P.group('albumId')
            cid = seed_P.group('cid')
            self.program['mainId'] = albumId
            seed_sub = 'http://cache.video.qiyi.com/jp/avlist/%s/' %(albumId)
            self.secondSpider(seed_sub)
            return

    def secondSpider(self, seed):
        doc = spiderTool.getHtmlBody(seed)
        try:
            json_data = json.loads(doc.split('=', 1)[1])
        except:
            return
        data = json_data["data"]
        if 'vlist' in data:
            data = data['vlist']
        for each in data:
            self.program_sub = copy.deepcopy(PROGRAM_SUB)
            setNumber = ''
            setName = ''
            webUrl = ''
            poster = ''
            playLength = ''
            setIntro = ''
            if 'tvYear' in each:
                setNumber = each['tvYear']
            elif 'pds' in each:
                setNumber = each['pds']
            if 'videoName' in each:
                setName = each['videoName']
            elif 'shortTitle' in each:
                setName = each['shortTitle']
            if 'vUrl' in each:
                webUrl = each['vUrl']
            elif 'vurl' in each:
                webUrl = each['vurl']
            if 'aPicUrl' in each:
                poster = each['aPicUrl']
            elif 'vpic' in each:
                poster = each['vpic']
            if 'timeLength' in each:
                playLength = each['timeLength']
            if 'desc' in each:
                setIntro = each['desc']
            if re.search(r'预告'.decode('utf8'), setName) or setNumber == "" or setName == "" or webUrl == ""\
                    or setNumber is None or setName is None or webUrl is None:
                continue
            self.program_sub['setNumber'] = setNumber.replace('-', '')
            self.program_sub['setName'] = setName
            self.program_sub['webUrl'] = webUrl
            self.program_sub['poster'] = poster
            self.program_sub['playLength'] = str(int(playLength)/60) + ':' + str(int(playLength)%60)
            self.program_sub['setIntro'] = setIntro
            self.program['programSub'].append(self.program_sub)

if __name__ == '__main__':
    app = iqiyi_short_1()
    app.doProcess()