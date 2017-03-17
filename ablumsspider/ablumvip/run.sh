#!/bin/sh

export baseDir=$(cd "$(dirname "$0")"; pwd)
export crawlerdata_RemotePath="tvfan@103.244.165.195:/opt/crawler_data/import/"

logPath=$baseDir/log
if [ ! -d $logPath ];then
        mkdir $logPath
fi


##
##
##
#add log file
logfile=${logPath}/`date +'%Y%m%d'`".log"
cd $baseDir

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./youku/run.sh" >> $logfile
./youku/run.sh

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./iqiyi/run.sh" >> $logfile
./iqiyi/run.sh

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./le/run.sh" >> $logfile
./le/run.sh

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./mgtv/run.sh" >> $logfile
./mgtv/run.sh

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./sohu/run.sh" >> $logfile
./sohu/run.sh

echo `date +[%Y/%m/%d-%H:%M:%S]` >> $logfile
echo "./pptv/run.sh" >> $logfile
./pptv/run.sh

