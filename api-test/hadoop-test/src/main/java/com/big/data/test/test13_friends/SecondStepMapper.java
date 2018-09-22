package com.big.data.test.test13_friends;


import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.Arrays;

public class SecondStepMapper extends Mapper<LongWritable, Text, Text, Text> {

    private Text k = new Text();
    private Text v = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split(":");

        v.set(fields[0]);

        String[] users = fields[1].split(",");

        Arrays.sort(users);
        // <用户,用户> 友
        for (int i = 0; i < users.length - 1; i++) {
            for (int j = i + 1; j < users.length; j++) {
                k.set("<" + users[i] + "," + users[j] + ">");
                context.write(k, v);
            }
        }

    }

}
         

