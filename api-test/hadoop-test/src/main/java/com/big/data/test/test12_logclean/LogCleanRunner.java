package com.big.data.test.test12_logclean;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class LogCleanRunner {

    public static void main(String[] args) throws Exception {

        args = new String[]{"api-test/hadoop-test/test12/in", "api-test/hadoop-test/test12/out"};

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf);

        job.setJarByClass(LogCleanRunner.class);

        job.setMapperClass(LogCleanMapper.class);
        // 无 Reducer 阶段 , 必须强制设置 reducer 个数为 0, 否则会开启空 Reducer
        job.setNumReduceTasks(0);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        boolean completion = job.waitForCompletion(true);
        System.exit(completion ? 0 : 1);


    }

}
         
