#!/bin/sh

#check
if [ x"$basePath" = x ]
then
	baseDir=$(cd "$(dirname "$0")"; pwd)
        baseDir=${baseDir%/*}
fi
if [ x"$crawlerdata_RemotePath" = x ]
then
	crawlerdata_RemotePath="tvfan@103.244.165.195:/opt/crawler_data/import/"
fi

basePath=$baseDir/pptv

dataPath=$basePath/data
dataBake=$basePath/bake
logPath=$basePath/log

#work directory check
if [ ! -d $basePath ];then
        echo "basePath error!"
        exit 1
fi
if [ ! -d $dataPath ];then
        mkdir $dataPath
fi
if [ ! -d $dataBake ];then
        mkdir $dataBake
fi
if [ ! -d $logPath ];then
        mkdir $logPath
fi


#add log file
logfile=${logPath}/`date +'%Y%m%d'`".log"
cd $basePath
echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "python ./all_pptv_vipmovie.py >> $logfile" >> $logfile
python ./all_pptv_vipmovie.py >> $logfile

#make bak directory
if [ ! -d $dataBake/`date +'%Y%m%d'` ];then
        mkdir $dataBake/`date +'%Y%m%d'`
fi

#copy data to craw remote directory, recored the log and make bake
bake=$dataBake/`date +'%Y%m%d'`
data=`ls $dataPath`
for item in $data
do
	#scp $dataPath/$item  $crawlerdata_RemotePath
	echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
	echo "cp $$dataPath/$item to $crawlerdata_RemotePath" >> $logfile
	mv $dataPath/$item $bake
done
