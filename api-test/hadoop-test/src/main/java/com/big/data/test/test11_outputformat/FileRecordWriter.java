package com.big.data.test.test11_outputformat;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;

import java.io.IOException;


public class FileRecordWriter extends RecordWriter<Text, NullWritable> {

    private FileSystem fs = null;

    private FSDataOutputStream atguiguFos = null;
    private FSDataOutputStream otherFos = null;

    public FileRecordWriter() {
    }

    public FileRecordWriter(TaskAttemptContext context) {
        try {
            Configuration conf = context.getConfiguration();
            fs = FileSystem.newInstance(conf);

            Path atgugiuPath = new Path("api-test/hadoop-test/test11/start.log");
            Path otherPath = new Path("api-test/hadoop-test/test11/other.log");

            atguiguFos = fs.create(atgugiuPath);
            otherFos = fs.create(otherPath);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Override
    public void close(TaskAttemptContext context) throws IOException,
            InterruptedException {
        IOUtils.closeStream(atguiguFos);
        IOUtils.closeStream(otherFos);
        IOUtils.closeStream(fs);
    }

    @Override
    public void write(Text text, NullWritable value) throws IOException,
            InterruptedException {

        // 换行符  linux : \n , win: \r\n
        String line = text.toString() + "\r\n";

        // 写出字节码,防乱码
        if (line.contains("start")) {
            atguiguFos.write(line.getBytes());
        } else {
            otherFos.write(line.getBytes());
        }

    }

}
         
