package com.big.data.hbase.save;


import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/*
     vim fruit.tsv
    --------------------------------
    1001    Apple   Red
    1002    Pear    Yellow
    1003    Pineapple       Yellow
    --------------------------------

    hdfs dfs -put fruit.tsv /tmp

    hbase-shell> createt 'fruit' 'info'
    执行导入命令
    yarn jar /Users/huhao/software/idea_proj/data-base/api-test/hbase-test/target/hbase-test-1.0-SNAPSHOT.jar com.big.data.hbase.save.TSV2HBaseRunner /tmp/fruit.tsv fruit_cp
 */
public class TSV2HBaseRunner extends Configured implements Tool{

    private static Log LOG = LogFactory.getLog(TSV2HBaseRunner.class);

    private static Configuration conf = null;

    public int run(String[] args) throws Exception {

        Job job = Job.getInstance(conf);
        job.setJarByClass(TSV2HBaseRunner.class);

        job.setMapperClass(TSVReadMapper.class);

        job.setMapOutputKeyClass(ImmutableBytesWritable.class);
        job.setMapOutputValueClass(Put.class);

        FileInputFormat.setInputPaths(job, args[0]);

        TableMapReduceUtil.initTableReducerJob(args[1], HTableWriteReducer.class, job);

        job.setNumReduceTasks(1);

        boolean status = job.waitForCompletion(true);


        if (status) {
            LOG.info("TSV2HBaseRunner has run " + status + ". >>>");
        } else {
            LOG.error("TSV2HBaseRunner has run " + status + ". >>>");
        }

        return status ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {
        TSV2HBaseRunner runner = new TSV2HBaseRunner();

        conf = HBaseConfiguration.create();
        runner.setConf(conf);

        int status = ToolRunner.run(conf, runner, args);

        System.exit(status);
    }
}
         
