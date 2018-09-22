package com.big.data.hbase.copy;


import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.io.NullWritable;

import java.io.IOException;

/**
 * TableReducer<KEYIN, VALUEIN, KEYOUT> extends Reducer<KEYIN, VALUEIN, KEYOUT, Mutation>
 * 1.TableReducer的输出Value类型固定:Mutation抽象类,且Get,Put,Delete,Increment 都是其子类
 * 2.直接遍历逐个发送即可
 *
 * @author Administrator
 */

public class HTableWriteReducer extends TableReducer<ImmutableBytesWritable, Put, NullWritable> {
    @Override
    protected void reduce(ImmutableBytesWritable keyIn, Iterable<Put> iterators, Context context) throws InterruptedException,IOException {
        for (Put put : iterators) {
            context.write(NullWritable.get(), put);
        }
    }
}
