#!/usr/bin/env python
#encoding=UTF-8
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from route import login
from route import index
from route import statistic
from route import spider
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from model.mysqldb import db
bootstrap = Bootstrap()

def createApp():
    app = Flask('spiderManager', template_folder=os.path.abspath('views'))
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    db.init_app(app)
    bootstrap.init_app(app)
    app.config['SECRET_KEY'] = 'super secret key'
    app.register_blueprint(index.bp, url_prefix='')
    app.register_blueprint(login.bp, url_prefix='/account')


    app.register_blueprint(statistic.bp, url_prefix='/statistic')
    app.register_blueprint(spider.bp, url_prefix="/spider")

    return app

if __name__ == "__main__":
    app = createApp()
    app.run(host="0.0.0.0", port=9527, debug=True)



