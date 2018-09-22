#!/bin/bash

# crontab
# */3 * * * * huhao cd /Users/huhao/software/virtual_space/running_jars/app-log && nohup sh -x hdfstohive.sh >> ./hdfstohive.log 2>&1 &

# macos
now=`date "+%s"`
before_3_mins=`expr $now - 180`
systime=`date -r $before_3_mins +%Y%m-%d-%H%M`

# linux
#systime=`date -d "-3 minute" +%Y%m-%d-%H%M`
ym=`echo ${systime} | awk -F '-' '{print $1}'`
day=`echo ${systime} | awk -F '-' '{print $2}'`
hm=`echo ${systime} | awk -F '-' '{print $3}'`

echo "------- $systime --------"

#执行hive的命令

hive -e "load data inpath '/user/centos/applogs/startup/${ym}/${day}/${hm}' into table applogsdb.ext_startup_logs partition(ym='${ym}',day='${day}',hm='${hm}')"
hive -e "load data inpath '/user/centos/applogs/error/${ym}/${day}/${hm}' into table applogsdb.ext_error_logs partition(ym='${ym}',day='${day}',hm='${hm}')"
hive -e "load data inpath '/user/centos/applogs/event/${ym}/${day}/${hm}' into table applogsdb.ext_event_logs partition(ym='${ym}',day='${day}',hm='${hm}')"
hive -e "load data inpath '/user/centos/applogs/usage/${ym}/${day}/${hm}' into table applogsdb.ext_usage_logs partition(ym='${ym}',day='${day}',hm='${hm}')"
hive -e "load data inpath '/user/centos/applogs/page/${ym}/${day}/${hm}' into table applogsdb.ext_page_logs partition(ym='${ym}',day='${day}',hm='${hm}')"
