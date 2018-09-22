package com.big.data.test.test10_merge_input;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

import java.io.IOException;


public class WholeFileRecordReader extends RecordReader<NullWritable, BytesWritable> {
        
    private FileSplit fSplit = null;
    private FileSystem fs = null;
    private FSDataInputStream fis = null;

    private boolean isCompleted = false;

    private BytesWritable value = new BytesWritable();


    @Override
    public void close() throws IOException {
        IOUtils.closeStream(fis);
        IOUtils.closeStream(fs);
    }
        

    @Override
    public NullWritable getCurrentKey() throws IOException,
            InterruptedException {
        return NullWritable.get();
    }
        

    @Override
    public BytesWritable getCurrentValue() throws IOException,
            InterruptedException {
        return value;
    }
        

    @Override
    public float getProgress() throws IOException, InterruptedException {
        return isCompleted ? 1 : 0;
    }
        

    @Override
    public void initialize(InputSplit split, TaskAttemptContext context)
            throws IOException, InterruptedException {
        
        fSplit = (FileSplit) split;

        Configuration conf = context.getConfiguration();

        fs = FileSystem.newInstance(conf);

    }
        

    @Override
    public boolean nextKeyValue() throws IOException, InterruptedException {

        boolean result = false;

        if (!isCompleted) {

            Path path = fSplit.getPath();

            fis = fs.open(path);

            byte[] buf = new byte[(int) fSplit.getLength()];

            IOUtils.readFully(fis, buf, 0, buf.length);
        
            value.set(buf, 0, buf.length);

            isCompleted = true;

            result = true;

        }

        return result;
    }

}
         

