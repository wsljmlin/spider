#!/usr/bin/env python
#encoding=UTF-8
import sys
import os
import re
import time
import json
from pymongo import MongoClient

class mongodb():
    def __init__(self):
        self.today = time.strftime('%Y%m%d', time.localtime())
        self.conn = MongoClient('10.1.1.6',27017)
        self.db = self.conn['spider']
        self.db.authenticate('tvfan','tvfanSpider')
        self.program = self.db["program"]
        self.collections = self.db.collection_names()
        if self.today not in self.collections:
            self.db.create_collection(self.today)
        self.log = self.db[self.today]
        self.inputFile = ".\data\mgtv_tv_20160718.txt" #".\data\\all_ppypp_tv_20160715.txt"
        self.outputFile = ".\data\out.txt"

    def doProcess(self):
        if not os.path.isfile(self.inputFile):
            return
        writeFile = mongodb.openFile(self.outputFile)
        readFile = open(self.inputFile,'r')
        line = readFile.readline()
        while line:
            data = {}
            try:
                data = json.loads(line)
            except:
                pass
            if self.mergeProgram(data) is not None:
                if len(data["program"]["programSub"]) > 0:
                    if data.has_key('_id'):
                        data.pop('_id')
                    writeFile.write(json.dumps(data) + "\n")
            line = readFile.readline()

    def mergeProgram(self, data):
        nameTag = "name"
        mainIdTag = "mainId"
        programTag = "program"
        programSubTag = "programSub"
        name = ""
        program = ""
        mainId = ""
        programSub = ""
        if data.has_key(programTag):
            program = data[programTag]
        if program.has_key(nameTag):
            name = program[nameTag]
        if program.has_key(mainIdTag):
            mainId = program[mainIdTag]
        if program.has_key(programSubTag):
            programSub = program[programSubTag]
        if name == "" or program == "" or mainId == "" or len(programSub) == 0 :
            return None

        oldData = self.program.find_one({nameTag: name, mainIdTag: mainId})
        if oldData:
            self.mergeSubProgram(oldData, data)
            self.program.save(oldData)
        else:
            data[nameTag] = name
            data[mainIdTag] = mainId
            self.program.save(data)
            self.writeToLog(programSub)
        return True

    def mergeSubProgram(self, old, new):
        newSub = []
        setNumberTag = "setNumber"
        setNameTag = "setName"
        programTag = "program"
        programSubTag = "programSub"
        subDick = {}
        oldSubList = []
        if old[programTag].has_key(programSubTag):
            oldSubList = old[programTag][programSubTag]
        else:
            old[programTag][programSubTag] = oldSubList
        for sub in oldSubList:
            setNumber = ""
            setName = ""
            if sub.has_key(setNumberTag):
                setNumber = sub[setNumberTag]
            if sub.has_key(setNameTag):
                setName = sub[setNameTag]
            if setName != "" and setNumber != "":
                subDick[setNumber] = setName
        newSubList = []
        if new[programTag].has_key(programSubTag):
            newSubList = new[programTag][programSubTag]
        for sub in newSubList:
            setNumber = ""
            setName = ""
            if sub.has_key(setNumberTag):
                setNumber = sub[setNumberTag]
            if sub.has_key(setNameTag):
                setName = sub[setNameTag]
            if setName == "" or setNumber == "":
                continue
            if subDick.has_key(setNumber):
                continue
            oldSubList.append(sub)
            newSub.append(sub)
        new[programTag][programSubTag] = newSub
        if len(newSub) > 0:
            self.writeToLog(newSub)
    def writeToLog(self,newSub):
        tagList = self.inputFile.split(os.path.sep)[-1].split('\\')[-1].split('/')[-1].split('_')
        if re.search(r'all', self.inputFile):
            source = tagList[1]
            category = tagList[2]
            spider = "all"
        else:
            source = tagList[1]
            category = tagList[2]
            spider = tagList[0]
        subCount = len(newSub)
        self.log.update({"source": source, "category": category, "spider": spider},{"$inc":{"programCount":1,"subProgramCount": subCount}},True,)

    @staticmethod
    def openFile(dataFile):
        try:
            openFile = open(dataFile, 'w')
            return openFile
        except:
            print "file open error!"
        return None

#user = {'name':'ximing'}
#collect.save(user)
#打印所有聚集名称，连接聚集
#        collect.update({"name":"ximing"}, {'$push': {"age": 4}})

#        for user in collect.find():
#                print user


if __name__ == '__main__':
    app = mongodb()
    app.doProcess()
    if len(sys.argv) > 2:
        if os.path.isfile(sys.argv[1]):
            app.inputFile = sys.argv[1]
            app.outputFile = sys.argv[2]
            app.doProcess()
        else:
            print "inputFile is not exist."
    else:
        print "argv error !"
