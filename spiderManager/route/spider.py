#!/usr/bin/env python
#encoding=UTF-8
import sys
import os
import time
import re
import types
import json
from bs4 import BeautifulSoup
from flask import Blueprint
from flask import render_template
from flask import request
from model.loginVerify import requireLogin
from flask_wtf import Form
from wtforms import form
from wtforms import TextField, StringField, SelectField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired
from model.spiderModel import spiderModel
from model.spiderCron import spiderCron
from model.mysqldb import db
from spiderModel.spiderTool import spiderTool
from config import spiderModelPath
from config import runtimeSave
sys.path.append(spiderModelPath)

class sourceForm(Form):
    source = SelectField(u'视频源：', validators=[validators.Length(min=1, max=25)])
    type = SelectField(u'视频分类：', validators=[validators.Length(min=1, max=25)])
    spiderModel = SelectField(u'爬虫模块：', validators=[validators.Length(min=1, max=25)])
    example = SelectField(u'示例种子：')
    url = StringField(u'播放地址：')
    submitButton = SubmitField(u'开始爬取')


class cronForm(Form):
    cron_id = StringField(u'定时id：', validators=[validators.Length(min=1, max=25)])
    name = StringField(u'节目名称：', validators=[validators.Length(min=1, max=25)])
    url = StringField(u'种子url：', validators=[validators.Length(min=1, max=25)])
    spider = StringField(u'爬虫模块：', validators=[validators.Length(min=1, max=25)])
    runTime = StringField(u'执行时间：')
    submitButton = SubmitField(u'保存')

class mfspForm(Form):
    type = SelectField(u'视频分类：',validators=[validators.Length(min=1, max=25)])
    word = StringField(u'搜索内容：',validators=[validators.Length(min=1, max=25)])
    submitButton = SubmitField(u'开始搜索')


bp = Blueprint('spider', __name__)

@bp.route('/')
@requireLogin
def spider():
    return render_template('spider/spider.html')

@bp.route('/cron')
@requireLogin
def all():
    totalPage =1
    return render_template('spider/spiderCron.html',totalPage=totalPage, runtimeSave=runtimeSave)

@bp.route('/find',methods=['GET', 'POST'])
@requireLogin
def find():
    getKeys = request.args.keys()
    name = "%%"
    pageNum = 1
    totalPage = 1
    pageListNum = 20
    if "nameGet" in getKeys:
        name = "%" + request.args.get("nameGet") + "%"
    if "pageNum" in getKeys:
        pageNum = int(request.args.get("pageNum").encode('utf8'))
    SpiderCron = spiderCron()
    data =[{"cron_id": u.id, "name": u.name, "url": u.url, "spider": u.spider, "runTime": {u.runTime: runtimeSave[int(str(u.runTime).encode('utf8'))]}}
           for u in db.session.query(spiderCron).filter(spiderCron.name.ilike(name))]
    totalPage = len(data)//pageListNum
    if len(data) % pageListNum > 0:
        totalPage += 1
    if int(pageNum) > totalPage:
        pageNum = 1
    pageData = []
    beginIndex = pageListNum*(pageNum-1)
    endIndex = pageListNum*pageNum
    if endIndex > len(data):
        endIndex = len(data)
    for i in range(beginIndex, endIndex):
        pageData.append(data[i])
    rtData = {"totalPage": totalPage, "pageNum": pageNum, "data": pageData}
    rtStr = json.dumps(rtData)
    return rtStr

@bp.route('/album',methods=['GET', 'POST'])
@requireLogin
def album():
    jsonData = ""
    nameSave = ""
    urlSave = ""
    spiderSave = ""

    form = sourceForm()
    form.source.choices = [(u.source, u.source) for u in db.session.query(spiderModel.source).group_by(spiderModel.source)]
    form.type.choices = [(u.type, u.type) for u in db.session.query(spiderModel.type).group_by(spiderModel.type)]
    form.spiderModel.choices = [(u.spider, u.spider) for u in db.session.query(spiderModel.spider).group_by(spiderModel.spider)]
    form.example.choices = [(u.url, u.url) for u in db.session.query(spiderModel.url).group_by(spiderModel.url)]
    form.submitButton = u'开始爬取'
    if form.validate_on_submit():
        requestForm = request.form
        keyList = requestForm.keys()
        source = ""
        type = ""
        spiderF = ""
        example = ""
        submitButton = ""
        url = ""
        if "source" in keyList:
            source = requestForm["source"]
        if "type" in keyList:
            type = requestForm["type"]
        if "spiderModel" in keyList:
            spiderModelName = requestForm["spiderModel"]
        if "example" in keyList:
            example = requestForm["example"]
        if 'submitButton' in keyList:
            submitButton = requestForm['submitButton']
        if 'url' in keyList:
            url = requestForm['url']
        if submitButton == '1' and source != "":
            form.type.choices = [(u.type, u.type) for u in db.session.query(spiderModel.type).filter(spiderModel.source == source).group_by(spiderModel.type)]
            form.spiderModel.choices = [(u.spider, u.spider) for u in db.session.query(spiderModel.spider).filter(spiderModel.source == source).group_by(spiderModel.spider)]
        elif submitButton == '2' and type != "" and source != "":
            form.spiderModel.choices = [(u.spider, u.spider) for u in db.session.query(spiderModel.spider).filter(spiderModel.source == source, spiderModel.type == type).group_by(spiderModel.spider)]
            if len(form.spiderModel.choices) == 1:
                form.example.choices = [(u.url, u.url) for u in db.session.query(spiderModel.url).filter(spiderModel.source == source, spiderModel.type == type).group_by(spiderModel.url)]
        elif submitButton == '3'and spiderModelName != "" and type != "" and source != "":
            form.spiderModel.choices = [(spiderModelName, spiderModelName) ]
            form.type.choices = [(u.type, u.type) for u in db.session.query(spiderModel.type).filter(spiderModel.spider == spiderModelName).group_by(spiderModel.type)]
            form.example.choices = [(u.url, u.url) for u in db.session.query(spiderModel.url).filter(spiderModel.spider == spiderModelName).group_by(spiderModel.url)]
        elif submitButton != '1' and submitButton != '2' and url != "":
            spider_class = ""
            modelList = os.listdir(spiderModelPath)
            if spiderModelName + ".py" not in modelList:
                jsonData = u"{'msg':'该爬取模块不存在！'}"
            else:
                try:
                    spider_module = __import__(spiderModelName)
                    spider_class = eval("spider_module." + spiderModelName + "()")
                except:# IOError, e:
                    jsonData = u"{'msg':'该爬取模块无法初始化！'}"

            if spider_class != "":
                try:
                    spider_class.seedList = [url]
                    spider_class.seedSpider()
                    jsonData = spider_class.jsonData
                    urlSave = url
                    spiderSave = spiderModelName
                    nameSave = spider_class.program['name']
                    if jsonData == "":
                        jsonData = u"{'msg':'爬取失败，请选用其他模块，或联系工程师！'}"
                except:# IOError, e:
                    jsonData = u"{'msg':'爬取失败，请选用其他模块，或联系工程师！'}"
        elif submitButton != '1' and submitButton != '2' and url == "":
            jsonData = u"{'msg':'url不能为空！'}"
    return render_template('spider/spiderTmp.html', form=form, jsonData=jsonData, urlSave=urlSave, nameSave=nameSave, spiderSave=spiderSave, runtimeSave=runtimeSave)

@bp.route('/shangchuan', methods=['GET', 'POST'])
@requireLogin
def shangchuan():
    jsonData = ""
    postKeys = request.form.keys()
    if 'jsonData' in postKeys:
        jsonData = request.form['jsonData']
    if type(jsonData) == types.UnicodeType:
        jsonData = jsonData.encode('utf8')
    if jsonData != "":
        fileName = 'data' + os.path.sep + time.strftime('cron_manager_spider_tmp_%Y%m%d%H%M%S.txt', time.localtime(time.time()))
        openFile = open(fileName,'w')
        openFile.write(str(jsonData))
        jsonData = u"{'msg':'数据已经上传，请耐心等待！'}"
        return jsonData
    jsonData = u"{'msg':'上传数据异常！'}"
    return jsonData

@bp.route('/save', methods=['GET', 'POST'])
@requireLogin
def save():
    postKeys = request.form.keys()
    id = ""
    name = ""
    url = ""
    spiderF = ""
    runtime = ""
    delete = False

    if "idSave" in postKeys:
        id = request.form["idSave"]

    if "delete" in postKeys:
        delete = True

    if id != "":
        SpiderCron = db.session.query(spiderCron).filter(spiderCron.id == id).first()
    else:
        SpiderCron = spiderCron()

    if "nameSave" in postKeys:
        name = request.form["nameSave"]
        SpiderCron.name = name
    if "urlSave" in postKeys:
        url = request.form["urlSave"]
        SpiderCron.url = url
    if "spiderSave" in postKeys:
        spiderF = request.form["spiderSave"]
        SpiderCron.spider = spiderF
    if "runtimeSave" in postKeys:
        runtime = request.form["runtimeSave"]
        SpiderCron.runTime = runtime

    if id == "":
        db.session.add(SpiderCron)
    elif id != "" and delete:
        db.session.delete(SpiderCron)

    db.session.commit()
    return "Data base connected."

@bp.route('/cronData', methods=['GET', 'POST'])
def cronData():
    getKeys = request.args.keys()
    if 'runTime' in getKeys:
        runTime = request.args['runTime']
        listData = [{'spider': u.spider, 'url': u.url} for u in db.session.query(spiderCron).filter(spiderCron.runTime == str(runTime))]
        strData = json.dumps(listData)
        return strData
    else:
        return ""



@bp.route('/mfsp',methods=['GET', 'POST'])
@requireLogin
def mfsp():
    form = mfspForm()
    form.type.choices=[('1', u'电影'),('2', u'电视剧'),('5', u'动漫'),('4', u'综艺'), ( '9',u'纪录片')]
    data = []
    if form.validate_on_submit():
        requestForm = request.form
        keyList = requestForm.keys()
        word = ""
        type = ""
        if "word" in keyList:
            word = requestForm["word"]
        if "type" in keyList:
            type = requestForm["type"]
        if word != "" and type != "":
            seed = "http://www.beevideo.tv/api/video2.0/video_search.action?channelId=%s&searchKey=%s" %(type, word)
            doc = spiderTool.getHtmlBody(seed)
            soup = BeautifulSoup(doc, from_encoding="utf8")
            video_list_p = soup.find('video_list')
            if video_list_p is not None:
                video_list = video_list_p.find_all('video_item')
                for each in video_list:
                    item = {}
                    url = ""
                    name = ""
                    type = ""
                    id = each.find('id')
                    if id is not None:
                        id_num = id.get_text()
                        url = 'http://www.beevideo.tv/api/video2.0/video_detail_info.action?videoId=' + id_num
                    name_tag = each.find('name')
                    if name_tag:
                        name = name_tag.get_text()
                    type_tag = each.find('channel')
                    if type_tag:
                        type = type_tag.get_text()
                    if name != "" and type != "" and url != "":
                        item = {"name":name, "type": type, "url": url}
                        data.append(item)

    return render_template('spider/mfsp.html',form=form, data=data)