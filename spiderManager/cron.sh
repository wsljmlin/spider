#!/bin/bash
#########################
. ~/.bashrc 
. ~/.profile
#########################
basePath="/spider/spiderManager"
dataPath=${basePath}/data
tmpPath=${basePath}/tmp
if [ ! -d $basePath ];then
	echo "basePath error!"
	exit 1
fi
if [ ! -d $dataPath ];then
	mkdir $dataPath
fi
cd $basePath
python cron.py `date +%H`
data=`ls ${dataPath}/cron_manager_spider_*`
for item in $data
do
    if [  -f ${item} ];then
        scp ${item}  tvfan@103.244.165.195:/opt/crawler_data/import/
        rm ${item}
    fi
done
