package com.big.data.test.test2_oodsPartition;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.Iterator;


public class WCReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
         
    private IntWritable value = new IntWritable();
         

    @Override
    protected void reduce(Text key, Iterable<IntWritable> iter, Context context)
            throws IOException, InterruptedException {
         
        // 1. 统计次数
        int count = 0;
         
        // 2.key相同value集合的迭代器
        Iterator<IntWritable> iterator = iter.iterator();
         
        // 3.遍历统计
        while (iterator.hasNext()) {
            IntWritable next = iterator.next();
            count += next.get();
        }
        // 4.封装结果
        value.set(count);
         
        // 5.输出结果
        context.write(key, value);
         
    }
         
}
         
