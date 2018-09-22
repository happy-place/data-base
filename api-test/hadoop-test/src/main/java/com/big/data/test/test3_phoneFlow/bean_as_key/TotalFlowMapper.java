package com.big.data.test.test3_phoneFlow.bean_as_key;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

// Mapper 中FlowBean最作为OutKey时,必须实现Comparable接口,如果仅作为OutValue输出,则可不实现Comparable接口
public class TotalFlowMapper extends Mapper<LongWritable, Text, FlowBean, FlowBean> {
        
    private FlowBean v = new FlowBean();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();

        String[] fields = line.split(" ");

        //k.set(fields[1]);

        v.set(fields[0], Long.parseLong(fields[1]), Long.parseLong(fields[2]));

        context.write(v, v);

    }

}
         
