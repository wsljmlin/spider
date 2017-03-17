#!/usr/bin/env python
#encoding=UTF-8
import time
import re
from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify
from model.loginVerify import requireLogin
from model.mongodb import cnn

bp = Blueprint('statistic', __name__)

@bp.route('/')
@requireLogin
def static():
    dateTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    data = cnn.static("", dateTime)
    return render_template('statistic/statistic.html', data=data, today=dateTime)

@bp.route('/data', methods=['GET', 'POST'])
@requireLogin
def data():
    spiderTag = request.args.get("tag","")
    dateTime = request.args.get("dateTime")
    if dateTime is not None and re.search(r'\d{10}',dateTime):
        dateTime = time.strftime('%Y%m%d', time.localtime(int(dateTime[:-3])))
    else:
        dateTime = time.strftime('%Y%m%d', time.localtime(time.time()))
    data = cnn.static(spiderTag, dateTime)
    return render_template('statistic/data.html', data=data)


