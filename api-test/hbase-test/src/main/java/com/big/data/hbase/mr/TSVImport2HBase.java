package com.big.data.hbase.mr;

public class TSVImport2HBase {

    /*
        1.hadooop 调用 hbase api 执行 mr
            export HADOOP_CLASSPATH=`${HBASE_HOME}/bin/hbase mapredcp`
            yarn jar /Users/huhao/software/cdh-2.5.0-5.3.6/hbase-0.98.6-cdh5.3.6/lib/hbase-server-0.98.6-cdh5.3.6.jar rowcounter "china_tele:call_log"
            等效于 hbase org.apache.hadoop.hbase.mapreduce.RowCounter 'china_tele:call_log'

        2. tsv 文件导入 hbase表
            vim fruit.tsv
            --------------------------------
            1001    Apple   Red
            1002    Pear    Yellow
            1003    Pineapple       Yellow
            --------------------------------

            hdfs dfs -put fruit.tsv /tmp

            hbase-shell> createt 'fruit' 'info'

            执行导入命令
            yarn jar $HBASE_HOME/lib/hbase-server-0.98.6-cdh5.3.6.jar importtsv \
            -Dimporttsv.columns=HBASE_ROW_KEY,info:name,info:color fruit \
            hdfs://localhost:9000/tmp/fruit.tsv

            hbase-shell> scan 'fruit'
            ROW                                             COLUMN+CELL
             1001                                           column=info:color, timestamp=1528869871893, value=Red
             1001                                           column=info:name, timestamp=1528869871893, value=Apple
             1002                                           column=info:color, timestamp=1528869871893, value=Yellow
             1002                                           column=info:name, timestamp=1528869871893, value=Pear
             1003                                           column=info:color, timestamp=1528869871893, value=Yellow
             1003                                           column=info:name, timestamp=1528869871893, value=Pineapple
            3 row(s) in 0.3190 seconds

     */


}
