package com.big.data.test.test13_friends;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class OneStepMapper extends Mapper<LongWritable, Text, Text, Text> {

    private Text k = new Text();
    private Text v = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split(":");
        // 用户  友友友
        v.set(fields[0]);

        for (String str : fields[1].split(",")) {
            k.set(str);
            // 友 用户
            context.write(k, v);
        }

    }

}
         


