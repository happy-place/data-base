#!/bin/bash

# 可以答题
workDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
sparkCommonLib="/data/sparkCommLib"
masterUrl="yarn-cluster"
master=`echo ${masterUrl} | awk -F'-' '{print $1}'`
deployMode=`echo ${masterUrl} | awk -F'-' '{print $2}'`
appName="HiveSelectInsert"

#.format(vid, answerable_late_input, cheez_wrong_noanswer_input, answerable_late_output)

# TODO >>>>>>>>> 上线后改为 offline <<<<<<<<<

source /etc/bashrc
/usr/hdp/current/spark2-client/bin/spark-submit --master ${master} \
--deploy-mode ${deployMode} \
--driver-memory 4g \
--executor-memory 2g \
--executor-cores 4 \
--num-executors 4 \
--queue offline \
--conf spark.memory.fraction=0.8 \
--conf spark.memory.storageFraction=0.3 \
--class com.big.data.spark.sql.onlinetest.HiveSelectInsert \
${workDir}/spark-hive-test.jar

# TODO >>>>>>> 上线后放开注释 <<<<<<<<
hdfs dfs -ls ${answerable_late_output}/part-*
answerable_late_code=$?

if [ "$answerable_late_code" != "0" ]
then
    echo "shortsTriviaReport/$0任务执行失败"
    # 发短信
    python /data/commLib/send_sms.py "shortsTriviaReport/$0 任务执行失败" "18601991068"
    exit 102
fi
