package com.big.data.test.test9_combine_small_splits;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class CombineInputFormatReducer extends Reducer<Text, NullWritable, Text, NullWritable> {

    @Override
    protected void reduce(Text key, Iterable<NullWritable> iter, Context context)
            throws IOException, InterruptedException {

        for (NullWritable nullWritable : iter) {
            context.write(key, nullWritable);
        }

    }

}
         
