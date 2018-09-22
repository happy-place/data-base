package com.big.data.test.test8_cache_join;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class OrderCachedReducer extends Reducer<OrderCachedBean, OrderCachedBean, OrderCachedBean, NullWritable> {

    @Override
    protected void reduce(OrderCachedBean key, Iterable<OrderCachedBean> iter, Context context)
            throws IOException, InterruptedException {

        for (OrderCachedBean orderCachedBean : iter) {
            context.write(orderCachedBean, NullWritable.get());
        }
    }

}
         


