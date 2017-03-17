#!/usr/bin/env python
#encoding=UTF-8

BASE_CONTENT = {
    'program':{         #节目信息
	'seqNo':'',	    #节目在当前cp中的序号
        'name':'',          #节目名称
        'alias':'',         #节目别名
        'ptype':'',         #节目类别：电视剧、电影等
        'channelName':'',   #频道名称：湖南卫视
        'shootYear':'',     #发行时间
        'intro':'',         #节目介绍
        'totalSets':-1,     #剧集数
        'point':-1.0,         #分数
        'doubanPoint':-1.0,   #豆瓣分数
        'playTimes':-1,     #播放量
        'mainId':'',        #优酷网该节目的唯一标识
        'getTime':'',       #信息获取时间
        'pcUrl':'',         #节目链接
        'urlValid':True,    #链接是否有效
        'website':'',       #网站名：优酷
		'tags':'',			#节目标签(中间用英文逗号分隔)，例如：成龙,武侠
		'viewPoint':'',		#节目看点
		'programLanguage':'', #节目语言
		'adaptor':'',		#编剧
		'tating':'',		#限制级别
		'awards':'',		#所获奖项(中间用英文逗号分隔)；如：奥斯卡金像奖,金狮奖
		'definition':'',	#清晰度
		'copyRight':'',		#版权信息
		'duration':'',		#总时长
		'income':'',		#票房
		'producer':'',		#制片人
		'cost':-1.0,		#制作成本
        'author':[          #作者
        ],
        'writer':[          #编剧
        ],
        'director':[        #导演
        ],
        'area':[            #区域
        #    {'name':'大陆'},
        #    {'name':'中国香港'}
        ],
        'ctype':[           #节目类型
        #    {'name':'神话'},
        #    {'name':'言情'}
        ],
        'star':[            #明星
        #    {'name':'胡歌'},
        #    {'name':'蒋劲夫'}
        ],
        'poster':[          #海报
        #    {'url':'http://res.mfs.ykimg.com/050E00004FB30C0E0000015BB409F9B7'},
        #    {'url':'http://res.mfs.ykimg.com/050E00004FB30C0E0000015BB409F9B7'}
        ],
        'programSub':[      #分集信息
        ],
    }
}

PROGRAM = {         #节目信息
        'name':'',          #节目名称
        'alias':'',         #节目别名
        'ptype':'',         #节目类别：电视剧、电影等
        'channelName':'',   #频道名称：湖南卫视
        'shootYear':'',     #发行时间
        'intro':'',         #节目介绍
        'totalSets':-1,     #剧集数
        'point':-1.0,         #分数
        'doubanPoint':-1.0,   #豆瓣分数
        'playTimes':-1,     #播放量
        'mainId':'',        #优酷网该节目的唯一标识
        'getTime':'',       #信息获取时间
        'pcUrl':'',         #节目链接
        'urlValid':True,    #链接是否有效
        'website':'',       #网站名：优酷
		'tags':'',			#节目标签(中间用英文逗号分隔)，例如：成龙,武侠
		'viewPoint':'',		#节目看点
		'programLanguage':'', #节目语言
		'adaptor':'',		#编剧
		'tating':'',		#限制级别
		'awards':'',		#所获奖项(中间用英文逗号分隔)；如：奥斯卡金像奖,金狮奖
		'definition':'',	#清晰度
		'copyRight':'',		#版权信息
		'duration':'',		#总时长
		'income':'',		#票房
		'producer':'',		#制片人
		'cost':-1.0,		#制作成本
        'author':[          #作者
        ],
        'writer':[          #编剧
        ],
        'director':[        #导演
        ],
        'area':[            #区域
        #    {'name':'大陆'},
        #    {'name':'中国香港'}
        ],
        'ctype':[           #节目类型
        #    {'name':'神话'},
        #    {'name':'言情'}
        ],
        'star':[            #明星
        #    {'name':'胡歌'},
        #    {'name':'蒋劲夫'}
        ],
        'poster':[          #海报
        #    {'url':'http://res.mfs.ykimg.com/050E00004FB30C0E0000015BB409F9B7'},
        #    {'url':'http://res.mfs.ykimg.com/050E00004FB30C0E0000015BB409F9B7'}
        ],
        'programSub':[      #分集信息
        ],
    }

PROGRAM_SUB = {
    'setName':'',      #分集名称
    'setNumber':'',    #第几集
    'poster':'',       #海报
    'playLength':'',   #分集时长
    'stars':'',        #参演明星
    'setIntro':'',     #分集介绍
    'webUrl':'',       #分集链接
    'urlValid':True,   #链接是否有效
    'plot':[           #字节目情节，发生时间(22:22)和标题
    #   {'time':'', 'title':''}
    ]
}
