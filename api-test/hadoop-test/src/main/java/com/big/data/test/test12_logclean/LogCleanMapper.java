package com.big.data.test.test12_logclean;


import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class LogCleanMapper extends Mapper<LongWritable, Text, Text, NullWritable> {

    private Counter passCount = null;
    private Counter dropCount = null;

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split(" ");

        if (fields.length >= 4) {
            context.write(value, NullWritable.get());
            passCount.increment(1l);
        } else {
            dropCount.increment(1l);
        }

    }

    @Override
    protected void setup(Context context)
            throws IOException, InterruptedException {

        passCount = context.getCounter("map", "pass");
        dropCount = context.getCounter("map", "drop");

    }

}
         



