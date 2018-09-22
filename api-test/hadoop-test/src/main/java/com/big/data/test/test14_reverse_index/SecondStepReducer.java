package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class SecondStepReducer extends Reducer<StringBean, StringBean, Text, NullWritable> {

    private Text k = new Text();
    private StringBuffer strBuf = new StringBuffer();

    @Override
    protected void reduce(StringBean key, Iterable<StringBean> iter, Context context)
            throws IOException, InterruptedException {

        strBuf.append(key.getTarget() + ":");

        for (StringBean bean : iter) {
            strBuf.append("\t" + bean.getPath() + "-->" + bean.getHint());
        }

        k.set(strBuf.toString());

        strBuf.delete(0, strBuf.length());

        context.write(k, NullWritable.get());

    }


}
         
