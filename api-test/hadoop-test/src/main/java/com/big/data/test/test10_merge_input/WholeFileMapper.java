package com.big.data.test.test10_merge_input;

import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class WholeFileMapper extends Mapper<NullWritable, BytesWritable,Text, BytesWritable> {

    private Text text = new Text();

    @Override
    protected void map(NullWritable key, BytesWritable value, Context context)
            throws IOException, InterruptedException {
        text.set(value.getBytes().toString());
        context.write(text, value);

    }


}
