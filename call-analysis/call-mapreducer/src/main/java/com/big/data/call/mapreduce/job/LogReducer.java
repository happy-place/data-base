package com.big.data.call.mapreduce.job;

import com.big.data.call.mapreduce.kv.impl.AnalysisValue;
import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.Iterator;

public class LogReducer extends Reducer<CombineDimension,IntWritable,CombineDimension,AnalysisValue> {

    private AnalysisValue valueOut = new AnalysisValue();

    @Override
    protected void reduce(CombineDimension key, Iterable<IntWritable> iter, Context context)
                throws IOException, InterruptedException {

        Iterator<IntWritable> iterator = iter.iterator ();

        int count = 0;
        int duration = 0;

        while(iterator.hasNext ()){
            count++;
            duration += iterator.next ().get ();
        }

        valueOut.setAll (count,duration);
        context.write (key,valueOut);
    }
}
