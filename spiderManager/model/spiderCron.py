#!/usr/bin/env python
#encoding=UTF-8
from model.mysqldb import db


class spiderCron(db.Model):
    __tablename__ = "spider_cron"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(40))
    url = db.Column(db.TEXT)
    spider = db.Column(db.VARCHAR(40))
    runTime = db.Column(db.Integer)
    createTime = db.Column(db.DateTime)
    text1 = db.Column(db.VARCHAR(20))
    text2 = db.Column(db.VARCHAR(20))

    # def __init__(self, source, type, spider, createTime):
    #     self.source = source
    #     self.type = type
    #     self.spider = spider
    #     self.createTime = createTime

    def __repr__(self):
        return '' % self.spider

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()