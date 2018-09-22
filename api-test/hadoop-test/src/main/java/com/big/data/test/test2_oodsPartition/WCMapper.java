package com.big.data.test.test2_oodsPartition;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class WCMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private Text k = new Text();
    private IntWritable v = new IntWritable();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        // 1.获取一行
        String line = value.toString();

        // 2.按指定分隔符拆分
        String[] words = line.split(" ");

        // 3.逐个单词封装到容器中发射出去,出现频数记为1
        for (String word : words) {
            k.set(word);
            v.set(1);
            context.write(k, v);
        }

    }

}
         

