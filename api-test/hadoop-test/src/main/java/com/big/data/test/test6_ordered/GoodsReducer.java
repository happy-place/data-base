package com.big.data.test.test6_ordered;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class GoodsReducer extends Reducer<Goods, Goods, Goods, NullWritable> {

    @Override
    protected void reduce(Goods key, Iterable<Goods> iter, Context context)
            throws IOException, InterruptedException {

        Goods next = iter.iterator().next();

        context.write(next, NullWritable.get());

    }

}
         
