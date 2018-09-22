package com.big.data.test.test4_sortedPhoneFlow;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

// Mapper 中FlowBean最作为OutKey时,必须实现Comparable接口,如果仅作为OutValue输出,则可不实现Comparable接口
public class OneStepSumMapper extends Mapper<LongWritable, Text, Text, FlowSortedBean> {

    private Text k = new Text();
    private FlowSortedBean v = new FlowSortedBean();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split("\t");

        k.set(fields[0]);

        v.set(fields[0], Long.parseLong(fields[1]), Long.parseLong(fields[2]));

        context.write(k, v);

    }

}
         
