#!/usr/bin/env python
#encoding=UTF-8
from flask import Blueprint
from flask import render_template
from flask import session
from model.loginVerify import requireLogin

bp = Blueprint('index', __name__)


@bp.route('/')
@bp.route('/index')
@requireLogin
def login():
    userName = session['userName'] if 'userName' in session else 'Guest'
    return render_template('index.html')

@bp.route('/test')
def test():
    return render_template('spiderTmp.html')