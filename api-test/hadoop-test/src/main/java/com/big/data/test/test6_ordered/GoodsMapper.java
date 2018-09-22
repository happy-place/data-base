package com.big.data.test.test6_ordered;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class GoodsMapper extends Mapper<LongWritable, Text, Goods, Goods> {
        
    private Goods bean = new Goods();
        

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        
        String line = value.toString();

        String[] fields = line.split(" ");

        bean.set(fields[0], fields[1], Double.parseDouble(fields[2]));

        context.write(bean, bean);
    }
        
}
         
