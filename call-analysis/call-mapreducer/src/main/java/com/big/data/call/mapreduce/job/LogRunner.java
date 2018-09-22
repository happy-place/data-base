package com.big.data.call.mapreduce.job;

import com.big.data.call.mapreduce.format.DBOutpuFormat;
import com.big.data.call.mapreduce.kv.impl.AnalysisValue;
import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class LogRunner extends Configured implements Tool {

    private static Log LOG = LogFactory.getLog (LogRunner.class);

    private static Configuration conf = new Configuration ();

    @Override
    public int run(String[] args) throws Exception {
        Job job = Job.getInstance (conf,LogRunner.class.getSimpleName ());
        job.setJarByClass (LogRunner.class);

        Scan scan = new Scan ();
        scan.setCacheBlocks (false);
        scan.setBatch (500);

        TableMapReduceUtil.initTableMapperJob ("china_tele:call_log",
                scan, LogMapper.class, CombineDimension.class, IntWritable.class,job,true);

        job.setReducerClass (LogReducer.class);

        job.setOutputKeyClass (CombineDimension.class);
        job.setOutputValueClass (AnalysisValue.class);

        job.setOutputFormatClass(DBOutpuFormat.class);

        return job.waitForCompletion (true)?0:1;
    }

    public static void main(String[] args) {
        LogRunner runner = new LogRunner();
        try {
            int code = ToolRunner.run (conf, runner, args);
            if(code == 0){
                LOG.info (">>> Job:<LogMapper,LogReducer> has run successfully...");
            }else{
                LOG.info (">>> Job:<LogMapper,LogReducer> has run failed...");
            }
        } catch (Exception e) {
            e.printStackTrace ();
        }
        String path = runner.getClass().getProtectionDomain().getCodeSource().getLocation().getPath ();
        System.out.println(path);
    }


}
