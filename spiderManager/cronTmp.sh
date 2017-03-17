#!/bin/bash
#########################
. ~/.bashrc 
. ~/.profile
#########################
basePath="/spider/spiderManager"
dataPath=${basePath}/data
if [ ! -d $basePath ];then
	echo "basePath error!"
	exit 1
fi
if [ ! -d $dataPath ];then
	mkdir $dataPath
fi
cd $basePath
data=`ls ${dataPath}/cron_manager_spider_tmp_*`
for item in $data
do
    if [  -f ${item} ];then
        scp ${item}  tvfan@103.244.165.195:/opt/crawler_data/import/
        rm ${item}
    fi
done
