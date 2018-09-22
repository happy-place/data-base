package com.big.data.test.test13_friends;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class SecondStepReducer extends Reducer<Text, Text, Text, NullWritable> {

    private Text k = new Text();
    private StringBuffer strBuf = new StringBuffer();

    @Override
    protected void reduce(Text key, Iterable<Text> iter, Context context)
            throws IOException, InterruptedException {

        // <用户,用户> 友友友...
        strBuf.append(key.toString() + "\t");

        for (Text text : iter) {
            strBuf.append(text.toString() + ",");
        }

        strBuf.deleteCharAt(strBuf.lastIndexOf(","));

        k.set(strBuf.toString());

        strBuf.delete(0, strBuf.length());

        context.write(k, NullWritable.get());
    }

}
         

