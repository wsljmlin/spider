#!/usr/bin/env python
#encoding=UTF-8
from model.mysqldb import db


class spiderModel(db.Model):
    __tablename__ = "spider_model"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.VARCHAR(20))
    type = db.Column(db.VARCHAR(20))
    spider = db.Column(db.VARCHAR(40))
    url = db.Column(db.VARCHAR(40))
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