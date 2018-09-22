package com.big.data.test.test2_oodsPartition;


import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Partitioner;

public class OddsPartitioner extends Partitioner<Text, IntWritable> {

    @Override
    public int getPartition(Text key, IntWritable value, int numReduceTasks) {

        // 默认分区必须从0开始
        int part = 0;

        //基于首字母ASCII排序
        int head = key.charAt(0);

        if (head % 2 != 0) {
            part = 1;
        }

        return part;
    }

}
         

