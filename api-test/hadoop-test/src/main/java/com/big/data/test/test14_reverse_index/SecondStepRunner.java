package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SecondStepRunner {

    public static void main(String[] args) throws Exception {

        args = new String[]{"api-test/hadoop-test/test14/out", "api-test/hadoop-test/test14/out2"};

        // 1.获取配置信息,创建任务对象
        Configuration conf = new Configuration();
        // 提交到yarn上运行
        //conf.set("mapreduce.framework.name", "yarn"); //  linux -yarn- mod
        //conf.set("yarn.resourcemanager.hostname", "hadoop101"); // win-yarn- mod

        Job job = Job.getInstance(conf);

        // 2.注册驱动类(可执行jar的入口)
        //job.setJar("f:/test/wc.jar");
        job.setJarByClass(SecondStepRunner.class);


        // 3.注册 Mapper ,Reducer类
        job.setMapperClass(SecondStepMapper.class);
        job.setReducerClass(SecondStepReducer.class);

        // 4.注册 Mapper 的输出K-V类型
        job.setMapOutputKeyClass(StringBean.class);
        job.setMapOutputValueClass(StringBean.class);

        job.setGroupingComparatorClass(GroupingComparator.class);

        // 5.注册最终输出结果的K-V类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);

        // 6.注册文件输入,结果输出路径
        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // 7.提交运行
        boolean completion = job.waitForCompletion(true);
        System.exit(completion ? 0 : 1);

    }


}
         
