package com.big.data.test.test4_sortedPhoneFlow;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class SecondStepSortMapper extends Mapper<LongWritable, Text, FlowSortedBean, NullWritable> {

    private FlowSortedBean bean = new FlowSortedBean();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split("\t");
        System.out.println(line + "\t"+fields.length);

        bean.set(fields[0].split("=")[1], Long.parseLong(fields[1].split("=")[1]), Long.parseLong(fields[2].split("=")[1]));

        context.write(bean, NullWritable.get());

    }

}
         
