package com.big.data.hbase.save;


import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;

public class TSVReadMapper extends Mapper<LongWritable, Text, ImmutableBytesWritable, Put>{
    private ImmutableBytesWritable keyOut = new ImmutableBytesWritable();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {


        String line = value.toString();
        String[] fields = line.split("\t");

        byte[] rowkey = Bytes.toBytes(fields[0]);
        Put put = new Put(rowkey);

        put.add(Bytes.toBytes("info"), Bytes.toBytes("name"), Bytes.toBytes(fields[1]));
        put.add(Bytes.toBytes("info"), Bytes.toBytes("color"), Bytes.toBytes(fields[2].toUpperCase()));

        keyOut.set(rowkey);

        context.write(keyOut, put);

    }

}
         
