package com.big.data.test.test9_combine_small_splits;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.CombineTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class CombineInputFormatRunner {

    public static void main(String[] args) throws Exception {

        args = new String[]{"api-test/hadoop-test/test9/in", "api-test/hadoop-test/test9/out"};

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf);

        job.setJarByClass(CombineInputFormatRunner.class);

        job.setMapperClass(CombineInputFormatMapper.class);
        job.setReducerClass(CombineInputFormatReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(NullWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);

//        job.setInputFormatClass(CombineTextInputFormat.class);
//        CombineTextInputFormat.setMaxInputSplitSize(job, 30);
//        CombineTextInputFormat.setMinInputSplitSize(job, 40);

        /*
         *  1)未使用CombineTextInputFormat: 按128M一个切片处理
         *  Processing split: Paths:/f:/ hadoop / combineipf /in/1. txt :0+26,/f:/ hadoop / combineipf /in/2. txt :0+24,/f:/ hadoop / combineipf /in/3. txt :0+21
         *  2)使用CombineTextInputFormat: 限制块大小[30,40]byte,分为两个切片提交
         *  Processing split: Paths:/f:/ hadoop / combineipf /in/1. txt :0+26,/f:/ hadoop / combineipf /in/2. txt :0+24
         *  Processing split: Paths:/f:/ hadoop / combineipf /in/3. txt :0+21
         */

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        boolean completion = job.waitForCompletion(true);
        System.exit(completion ? 0 : 1);

    }

}
         


