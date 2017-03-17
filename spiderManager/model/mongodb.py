#!/usr/bin/env python
#encoding=UTF-8
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from config import mongodb_ip
from config import mongodb_port
from config import mongodb_user
from config import mongodb_password
from config import mongodb_db

class mongodb():
    def __init__(self):
        self.conn = MongoClient(mongodb_ip, mongodb_port)
        self.db = self.conn[mongodb_db]
        self.db.authenticate(mongodb_user, mongodb_password)

    def static(self, spiderTag, Date):
        date_time = Date.replace("-","")
        data = []
        jsonList = []
        self.program = self.db["program"]
        self.collections = self.db.collection_names()
        if date_time not in self.collections:
            return data
        self.log = self.db[date_time]
        if spiderTag == 'else':
            jsonList = self.log.find({'spider': {'$nin': ['all', 'ablum']}}).sort([("source", ASCENDING), ("spider", ASCENDING), ("category", ASCENDING)])
        elif spiderTag != "":
            jsonList = self.log.find({'spider': spiderTag}).sort([("source", ASCENDING), ("spider", ASCENDING), ("category", ASCENDING)])
        else:
            jsonList = self.log.find().sort([("source", ASCENDING), ("spider", ASCENDING), ("category", ASCENDING)])
        for item in jsonList:
            if item.has_key('_id'):
                item.pop('_id')
            data.append(item)
        return data

cnn = mongodb()
if __name__ == '__main__':
    app = mongodb()
    aa =  app.static("2016-07-19")