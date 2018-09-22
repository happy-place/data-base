package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class SecondStepMapper extends Mapper<LongWritable, Text, StringBean, StringBean> {
    
    private StringBean bean = new StringBean();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split("\t");

        bean.setTarget(fields[0]);
        bean.setPath(fields[1]);
        bean.setHint(Integer.parseInt(fields[2]));

        context.write(bean, bean);

    }

}
         
