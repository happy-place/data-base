package com.big.data.hbase.save;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.io.NullWritable;

import java.io.IOException;

public class HTableWriteReducer extends TableReducer<ImmutableBytesWritable, Put, NullWritable> {

    @Override
    protected void reduce(ImmutableBytesWritable keyIn, Iterable<Put> iterator, Context context)
            throws IOException, InterruptedException {

        for (Put put : iterator) {
            context.write(NullWritable.get(), put);
        }
    }

}
         
