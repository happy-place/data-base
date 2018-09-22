package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class OneStepReducer extends Reducer<Text, IntWritable, Text, NullWritable> {

    private Text k = new Text();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> iter, Context context)
            throws IOException, InterruptedException {

        String[] fields = key.toString().split("\t");

        int count = 0;

        for (IntWritable intWritable : iter) {
            count += 1;
        }

        k.set(fields[0] + "\t" + fields[1] + "\t" + count);

        context.write(k, NullWritable.get());
    }

}
         
