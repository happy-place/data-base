package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

import java.io.IOException;

public class OneStepMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private Text k = new Text();
    private IntWritable v = new IntWritable();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        FileSplit split = (FileSplit) context.getInputSplit();
        String fileName = split.getPath().getName();

        String line = value.toString();
        String[] fields = line.split("\t");

        for (String field : fields) {
            k.set(field + "\t" + fileName);
            v.set(1);
            context.write(k, v);
        }

    }

}
         
