#!/usr/bin/env python
#encoding=UTF-8
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators
from wtforms.validators import DataRequired
class MyForm(Form):
    username = StringField(u'用户名', validators=[validators.Length(min=4, max=25)])
    password = PasswordField(u'密码', validators=[validators.Length(min=6, max=35)])
    submitButton = SubmitField(u'登陆')


bp = Blueprint('account', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'userName' in session:
        return redirect(request.args.get('next') or 'index')

    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == 'tvfan' and form.password.data == 'befun@tvfan':
            session['userName'] = form.username.data
            return redirect(session.pop('redirectUrl', None) or 'index')
        else:
            flash('用户名或密码错误!'.decode('utf8'))
            flash('Username or Password error!')

    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('userName', None)
    return redirect(url_for('account.login'))