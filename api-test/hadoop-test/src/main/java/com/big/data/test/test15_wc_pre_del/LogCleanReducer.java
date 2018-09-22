package com.big.data.test.test15_wc_pre_del;

import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class LogCleanReducer extends Reducer<LongWritable, Text, Text, NullWritable>{

	@Override
	protected void reduce(LongWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
		for(Text value : values){
			context.write(value, NullWritable.get());
		}
	}
	
}
