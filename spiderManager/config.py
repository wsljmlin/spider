#!/usr/bin/env python
#encoding=UTF-8
import os
basepath="/home/wangsl/Work/Spider/PaChong/spiderManager"#"D:\\tvfan_big_data\\spiderManager"#basepath="/spider/spiderManager"
mongodb_ip = "106.39.84.21"
mongodb_port = 27017
mongodb_user = "tvfan"
mongodb_password = "tvfanSpider"
mongodb_db = "spider"
#SQLALCHEMY_DATABASE_URI = "mysql://tvfan:tvfan2016spider@106.39.84.21:3308/spider"
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/spider"
spiderModelPath= basepath + os.path.sep + "spiderModel"
#定时任务启动时间
runtimeSave = {
    # 1: u"凌晨 01:00",
    # 2: u"凌晨 02:00",
    # 3: u"凌晨 03:00",
    # 4: u"凌晨 04:00",
    # 5: u"凌晨 05:00",
    # 6: u"早上 06:00",
    7: u"早上 07:00",
    8: u"早上 08:00",
    9: u"上午 09:00",
    10: u"上午 10:00",
    11: u"上午 11:00",
    12: u"中午 12:00",
    13: u"下午 01:00",
    14: u"下午 02:00",
    15: u"下午 03:00",
    16: u"下午 04:00",
    17: u"下午 05:00",
    18: u"下午 06:00",
    19: u"晚上 07:00",
    20: u"晚上 08:00",
    21: u"晚上 09:00",
    22: u"晚上 10:00",
    23: u"晚上 11:00",
    0: u"晚上 12:00",
}
