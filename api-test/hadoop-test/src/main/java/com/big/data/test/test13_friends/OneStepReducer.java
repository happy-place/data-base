package com.big.data.test.test13_friends;


import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class OneStepReducer extends Reducer<Text, Text, Text, NullWritable> {

    private Text k = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> iter, Context context)
            throws IOException, InterruptedException {

        StringBuffer strBuf = new StringBuffer(key.toString() + ":");
        // 友 用户 用户..
        for (Text text : iter) {
            strBuf.append(text.toString() + ",");
        }

        strBuf.deleteCharAt(strBuf.length() - 1);

        k.set(strBuf.toString());

        context.write(k, NullWritable.get());

    }

}
         


